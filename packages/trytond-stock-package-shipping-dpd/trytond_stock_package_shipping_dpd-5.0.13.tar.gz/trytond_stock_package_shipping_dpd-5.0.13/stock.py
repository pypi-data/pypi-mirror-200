# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import locale
from io import BytesIO
from itertools import zip_longest

from lxml import etree
from zeep.exceptions import Fault

try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    from PyPDF2 import PdfFileReader as PdfReader, PdfFileWriter as PdfWriter

from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.wizard import Wizard, StateAction, StateTransition
from trytond.transaction import Transaction

from .configuration import get_client, SHIPMENT_SERVICE

__all__ = ['ShipmentOut', 'CreateShipping', 'CreateDPDShipping']


def iter_pdf_pages(document):
    if hasattr(document, 'pages'):
        yield from document.pages
    else:
        for i in range(document.getNumPages()):
            yield document.getPage(i)


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    @classmethod
    def __setup__(cls):
        super(ShipmentOut, cls).__setup__()
        cls._error_messages.update({
                'warehouse_address_required': ('An address is required for'
                    ' warehouse "%(warehouse)s".'),
                })

    def validate_packing_dpd(self):
        warehouse_address = self.warehouse.address
        if not warehouse_address:
            self.raise_user_error('warehouse_address_required', {
                    'warehouse': self.warehouse.rec_name,
                    })


class CreateShipping(metaclass=PoolMeta):
    __name__ = 'stock.shipment.create_shipping'

    dpd = StateAction(
        'stock_package_shipping_dpd.act_create_shipping_dpd_wizard')

    def transition_start(self):
        pool = Pool()
        ShipmentOut = pool.get('stock.shipment.out')

        shipment = ShipmentOut(Transaction().context['active_id'])
        next_state = super(CreateShipping, self).transition_start()
        if shipment.carrier.shipping_service == 'dpd':
            next_state = 'dpd'
        return next_state

    def do_dpd(self, action):
        ctx = Transaction().context
        return action, {
            'model': ctx['active_model'],
            'id': ctx['active_id'],
            'ids': [ctx['active_id']],
            }


class CreateDPDShipping(Wizard):
    'Create DPD Shipping'
    __name__ = 'stock.shipment.create_shipping.dpd'

    start = StateTransition()

    @classmethod
    def __setup__(cls):
        super(CreateDPDShipping, cls).__setup__()
        cls._error_messages.update({
                'has_reference_number': ('Shipment "%(shipment)s" already has'
                    ' a reference number.'),
                'dpd_webservice_error': ('DPD webservice call failed with the'
                    ' following error message:\n\n%(message)s'),
                })

    def transition_start(self):
        pool = Pool()
        ShipmentOut = pool.get('stock.shipment.out')
        Package = pool.get('stock.package')

        shipment = ShipmentOut(Transaction().context['active_id'])
        if shipment.reference:
            self.raise_user_error('has_reference_number', {
                    'shipment': shipment.rec_name,
                    })

        credential = self.get_credential(shipment)
        if not credential.depot or not credential.token:
            credential.update_token()

        shipping_client = get_client(credential.server, SHIPMENT_SERVICE)
        print_options = self.get_print_options(shipment)
        packages = shipment.root_packages
        shipment_data = self.get_shipment_data(credential, shipment, packages)

        count = 0
        while count < 2:
            lang = (credential.company.party.lang.code
                if credential.company.party.lang else 'en')
            lang = locale.normalize(lang)[:5]
            authentication = {
                'delisId': credential.user_id,
                'authToken': credential.token,
                'messageLanguage': lang,
                }
            try:
                shipment_response = shipping_client.service.storeOrders(
                    print_options, shipment_data, _soapheaders={
                        'authentication': authentication,
                        })
                break
            except Fault as e:
                if e.detail:
                    tag = etree.QName(e.detail[0].tag)
                    if tag.localname == 'authenticationFault':
                        count += 1
                        credential.update_token()
                        continue
                raise
        else:
            self.raise_user_error('can_not_login', {
                    'credential': credential.rec_name,
                    })

        response, = shipment_response.shipmentResponses
        if response.faults:
            message = '\n'.join(f.message for f in response.faults)
            self.raise_user_error('dpd_webservice_error', {
                    'message': message,
                    })

        labels = []
        labels_pdf = BytesIO(shipment_response.parcellabelsPDF)
        reader = PdfReader(labels_pdf)
        for page in iter_pdf_pages(reader):
            new_pdf = PdfWriter()
            new_label = BytesIO()
            if hasattr(new_pdf, 'add_page'):
                new_pdf.add_page(page)
            else:
                new_pdf.addPage(page)
            new_pdf.write(new_label)
            labels.append(new_label)

        shipment.reference = response.mpsId
        parcels = response.parcelInformation
        for package, label, parcel in zip_longest(packages, labels, parcels):
            package.shipping_label = fields.Binary.cast(label.getvalue())
            package.shipping_reference = parcel.parcelLabelNumber
        Package.save(packages)
        shipment.save()

        return 'end'

    def get_credential_pattern(self, shipment):
        return {
            'company': shipment.company.id,
            }

    def get_credential(self, shipment):
        pool = Pool()
        DPDCredential = pool.get('carrier.credential.dpd')

        credential_pattern = self.get_credential_pattern(shipment)
        for credential in DPDCredential.search([]):
            if credential.match(credential_pattern):
                return credential

    def get_print_options(self, shipment):
        return {
            'printerLanguage': 'PDF',
            'paperFormat': 'A6',
            }

    def shipping_party(self, party, address):
        shipping_party = {
            'name1': address.party_full_name[:35],
            'name2': '',
            'street': ' '.join((address.street or '').splitlines())[:35],
            'country': address.country.code if address.country else '',
            'zipCode': address.zip[:9],
            'city': address.city[:35],
            }
        if party.full_name != address.party_full_name:
            shipping_party['name2'] = party.full_name[:35]

        phone = email = ''
        for mechanism in party.contact_mechanisms:
            if mechanism.type in {'phone', 'mobile'} and not phone:
                phone = mechanism.value
            if mechanism.type == 'email' and not email:
                email = mechanism.value
        if len(phone) <= 30:
            shipping_party['phone'] = phone
        if len(email) <= 50:
            shipping_party['email'] = email

        return shipping_party

    def get_parcel(self, package):
        pool = Pool()
        UoM = pool.get('product.uom')
        ModelData = pool.get('ir.model.data')

        cm = UoM(ModelData.get_id('product', 'uom_centimeter'))

        parcel = {}

        if package.total_weight:
            # in grams rounded in 10 gram units
            weight = int(package.total_weight * 10) * 10
            if weight < 1000000000:
                parcel['weight'] = weight

        if (package.type.length is not None
                and package.type.width is not None
                and package.type.height is not None):
            length = UoM.compute_qty(
                package.type.length_uom, package.type.length, cm)
            width = UoM.compute_qty(
                package.type.width_uom, package.type.width, cm)
            height = UoM.compute_qty(
                package.type.height_uom, package.type.height, cm)
            if length < 1000 and width < 1000 and height < 1000:
                parcel['volume'] = int(
                    '%03i%03i%03i' % (length, width, height))

        return parcel

    def get_shipment_data(self, credential, shipment, packages):
        return {
            'generalShipmentData': {
                'identificationNumber': shipment.number,
                'sendingDepot': credential.depot,
                'product': 'CL',
                'sender': self.shipping_party(
                    shipment.company.party, shipment.warehouse.address),
                'recipient': self.shipping_party(
                    shipment.customer, shipment.delivery_address),
                },
            'parcels': [self.get_parcel(p) for p in packages],
            'productAndServiceData': {
                'orderType': 'consignment',
                }
            }
