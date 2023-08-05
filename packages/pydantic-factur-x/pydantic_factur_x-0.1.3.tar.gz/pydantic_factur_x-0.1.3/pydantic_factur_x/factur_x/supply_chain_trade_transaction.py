"""Factur-X document context.

Insert specific Factur-X elements here.
"""
from enum import Enum
from typing import Optional, List
from pydantic_xml import BaseXmlModel, attr, element

from ._nsmaps import RSM, UDT, QTD, RAM, XSI
from .code_lists import UntDid1229
from .common import (
    BoolIndicator,
    IncludedNote,
    GlobalID,
    ValueMeasure,
    Quantity,
    Amount,
)
from .trade_party import TradeParty
from .document_reference import DocumentReference


class AssociatedDocumentLineDocument(
    BaseXmlModel,
    tag="AssociatedDocumentLineDocument",
    ns="ram",
    nsmap=RAM,
):
    """ram:AssociatedDocumentLineDocument

    Profiles:
        - Factur-X: basic
        - Order-X: basic
    """

    line_id: str = element(
        tag="LineID",
        ns="ram",
        profiles={"factur-x": "basic", "order-x": "basic"},
        description="""A unique identifier for the individual line within the document.""",
    )

    line_status_code: Optional[UntDid1229] = element(
        tag="LineStatusCode",
        ns="ram",
        profiles={"factur-x": "extended", "order-x": "basic"},
        description="""The identifier of the line in the associated document.""",
        usage="""Mandatory in invoices, optional in orders.""",
    )
    included_notes: Optional[List[IncludedNote]] = element(
        tag="IncludedNote",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "basic"},
        usage="""max one note for factur-X, no limit for order-X.""",
    )


class ApplicableProductCharacteristic(
    BaseXmlModel,
    tag="ApplicableProductCharacteristic",
    ns="ram",
    nsmap=RAM,
):
    """ram:ApplicableProductCharacteristic

    Profiles:
        - Factur-X: comfort
        - Order-X: comfort
    """

    type_code: Optional[str] = element(
        tag="TypeCode",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "comfort"},
        description="""A code specifying a type of product characteristic.""",
        usage="""To be chosen from the entries in UNTDID xxx""",
    )
    description: str = element(
        tag="Description",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "comfort"},
        description="""The name of the attribute or property of the item.""",
        usage="""Such as “Colour”.""",
    )
    value_measure: Optional[ValueMeasure] = element(
        tag="ValueMeasure",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "extended"},
        description="""A measure of a value for this product characteristic.""",
    )
    value: str = element(
        tag="Value",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "comfort"},
        description="""The value of the attribute or property of the item.""",
        usage="""Such as "Red".""",
    )


class SpecifiedTradeProduct(
    BaseXmlModel,
    tag="SpecifiedTradeProduct",
    ns="ram",
    nsmap=RAM,
):
    """ram:SpecifiedTradeProduct

    Profiles:
        - Factur-X: basic
        - Order-X: basic
    """

    id: Optional[str] = element(
        tag="ID",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "extended"},
        description="""An item identifier""",
    )
    global_id: Optional[GlobalID] = element(
        tag="GlobalID",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "basic"},
        description="""An item identifier based on a registered scheme.
        The identification scheme identifier of the Item standard identifier.""",
        usage="""The identification scheme shall be identified from the entries of the
        list published by the ISO/IEC 6523 maintenance agency.""",
    )
    seller_assigned_id: Optional[str] = element(
        tag="SellerAssignedID",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "basic"},
        description="""An identifier, assigned by the Seller, for the item.""",
    )
    buyer_assigned_id: Optional[str] = element(
        tag="BuyerAssignedID",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "basic"},
        description="""An identifier, assigned by the Buyer, for the item.""",
    )
    industry_assigned_id: Optional[str] = element(
        tag="IndustryAssignedID",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "extended"},
        description="""An identifier, assigned by the Industry, for the item.""",
    )
    model_id: Optional[str] = element(
        tag="ModelID",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "extended"},
        description="""A unique model identifier for this item.""",
    )
    name: str = element(
        tag="Name",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "basic"},
        description="""A name for an item.""",
        usage="""Mandatory in invoices, theorically optional in orders.""",
    )
    description: Optional[str] = element(
        tag="Description",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "comfort"},
        description="""A textual description of a use of this item.""",
    )
    batch_id: Optional[str] = element(
        tag="BatchID",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "extended"},
        description="""A batch identifier for this item.""",
    )
    brand_name: Optional[str] = element(
        tag="BrandName",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "extended"},
        description="""The brand name, expressed as text, for this item.""",
    )
    model_name: Optional[str] = element(
        tag="ModelName",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "extended"},
        description="""A group of business terms providing information about properties
        of the goods and services ordered.""",
    )
    applicable_product_characteristics: Optional[
        List[ApplicableProductCharacteristic]
    ] = element(
        tag="ApplicableProductCharacteristic",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "comfort"},
    )
    # designated_product_classifications # DesignatedProductClassification
    # individual_trade_product_instances # IndividualTradeProductInstance
    # applicable_supplychain_packaging  # ApplicableSupplychainPackaging
    # origin_trade_country # OriginTradeCountry
    # additional_reference_referenced_document # AdditionalReferenceReferencedDocument
    # included_referenced_product # IncludedReferencedProduct


class GrossPriceProductTradePrice(
    BaseXmlModel,
    tag="GrossPriceProductTradePrice",
    ns="ram",
    nsmap=RAM,
):
    """ram:GrossPriceProductTradePrice

    Profiles:
        - Factur-X: comfort
        - Order-X: comfort
    """

    charge_amount: str = element(
        tag="ChargeAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "comfort"},
        description="""The unit price, exclusive of VAT, before subtracting
        Item price discount.""",
    )
    basis_quantity: Optional[Quantity] = element(
        tag="BasisQuantity",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "comfort"},
        description="""The number of item units to which the price applies.""",
    )


class NetPriceProductTradePrice(
    BaseXmlModel,
    tag="NetPriceProductTradePrice",
    ns="ram",
    nsmap=RAM,
):
    """ram:NetPriceProductTradePrice

    Profiles:
        - Factur-X: basic
        - Order-X: basic
    """

    charge_amount: str = element(
        tag="ChargeAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "comfort"},
        description="""The unit price, exclusive of VAT, before subtracting
        Item price discount.""",
    )
    basis_quantity: Optional[Quantity] = element(
        tag="BasisQuantity",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "comfort"},
        description="""The number of item units to which the price applies.""",
    )
    minimum_quantity: Optional[Quantity] = element(
        tag="MinimumQuantity",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "extended"},
        description="""The minimum quantity in a range for which this trade
        price applies.""",
    )
    maximum_quantity: Optional[Quantity] = element(
        tag="MaximumQuantity",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "extended"},
        description="""The maximum quantity in a range for which this trade
        price applies.""",
    )
    # included_trade_tax  # IncludedTradeTax


class SpecifiedLineTradeAgreement(
    BaseXmlModel,
    tag="SpecifiedLineTradeAgreement",
    ns="ram",
    nsmap=RAM,
):
    """ram:SpecifiedLineTradeAgreement

    Profiles:
        - Factur-X: basic
        - Order-X: basic
    """

    minimum_product_orderable_quantity: Optional[Quantity] = element(
        tag="MinimumProductOrderableQuantity",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "extended"},
        description="""The minimum product orderable quantity for this
        line trade agreement.""",
    )
    maximum_product_orderable_quantity: Optional[Quantity] = element(
        tag="MaximumProductOrderableQuantity",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "extended"},
        description="""The maximum product orderable quantity for this
        line trade agreement.""",
    )
    # buyer_requisitioner_trade_party # BuyerRequisitionerTradeParty
    # buyer_order_referenced_document # BuyerOrderReferencedDocument
    # quotation_referenced_document # QuotationReferencedDocument
    # contract_referenced_document # ContractReferencedDocument
    # additional_referenced_docuement # AdditionalReferencedDocument
    # blanket_order_referenced_document # BlanketOrderReferencedDocument
    # ultimate_customer_order_referenced_document # UltimateCustomerOrderReferencedDocument

    gross_price_product_trade_price: Optional[GrossPriceProductTradePrice] = element(
        tag="GrossPriceProductTradePrice",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "comfort"},
        description="""A group of business terms providing information about the    """,
    )
    net_price_product_trade_price: NetPriceProductTradePrice = element(
        tag="NetPriceProductTradePrice",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "basic"},
    )

    # catalogue_referenced_document # CatalogueReferencedDocument
    # blanket_order_referenced_document # BlanketOrderReferencedDocument


class SpecifiedLineTradeDelivery(
    BaseXmlModel,
    tag="SpecifiedLineTradeDelivery",
    ns="ram",
    nsmap=RAM,
):
    """ram:SpecifiedLineTradeAgreement

    Profiles:
        - Factur-X: basic
        - Order-X: basic
    """

    partial_delivery_allowed_indicator: Optional[BoolIndicator] = element(
        tag="PartialDeliveryAllowedIndicator",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "basic"},
        description="""The indication, at line level, of whether or not this trade
        delivery can be partially delivered.""",
    )
    requested_quantity: Quantity = element(
        tag="RequestedQuantity",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "basic"},
        description="""The quantity, at line level, requested for
        this trade delivery.""",
    )
    agreed_quantity: Optional[Quantity] = element(
        tag="AgreedQuantity",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "basic"},
        description="""The quantity, at line level, agreed for this trade delivery.""",
    )
    package_quantity: Optional[Quantity] = element(
        tag="PackageQuantity",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "comfort"},
        description="""The number of packages, at line level, in this trade delivery.""",
    )
    per_package_unit_quantity: Optional[Quantity] = element(
        tag="PerPackageUnitQuantity",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "comfort"},
        description="""The number of units per package, at line level,
        in this trade delivery.""",
    )
    # ship_to_trade_party # ShipToTradeParty
    # ultimate_ship_to_party # UltimateShipToTradeParty
    # requested_despatch_supply_chain_event # RequestedDespatchSupplyChainEvent
    # requested_delivery_supply_chain_event # RequestedDeliverySupplyChainEvent


class ApplicableTradeTax(
    BaseXmlModel,
    tag="ApplicableTradeTax",
    ns="ram",
    nsmap=RAM,
):
    """ram:ApplicableTradeTax

    Profiles:
        - Factur-X: basic
        - Order-X: comfort
    """

    calculated_amount: Optional[float] = element(
        tag="CalculatedAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "extended"},
        description="""A monetary value resulting from the calculation of this trade
        related tax, levy or duty.""",
    )
    type_code: str = element(
        tag="TypeCode",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "comfort"},
        description="""The code specifying the type of trade related tax, levy or duty,
        such as a code for a Value Added Tax (VAT)
        [Reference United Nations Code List (UNCL) 5153]""",
        usage="""Value = VAT""",
    )
    exemption_reason: Optional[str] = element(
        tag="ExemptionReason",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "extended"},
        description="""The reason, expressed as text, for exemption from this trade
        related tax, levy or duty.""",
    )
    category_code: str = element(
        tag="CategoryCode",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "comfort"},
        description="""The VAT category code for the ordered item.""",
        usage="""The following entries of UNTDID 5305  are used
        (further clarification between brackets):
        - Standard rate (Liable for VAT in a standard way)
        - Zero rated goods (Liable for VAT with a percentage rate of zero)
        - Exempt from tax (VAT/IGIC/IPSI)
        - VAT Reverse Charge (Reverse charge VAT/IGIC/IPSI rules apply)
        - VAT exempt for intra community supply of goods (VAT/IGIC/IPSI not levied due
          to Intra-community supply rules)
        - Free export item, tax not charged (VAT/IGIC/IPSI not levied due to export
          outside of the EU)
        - Services outside scope of tax (Sale is not subject to VAT/IGIC/IPSI)
        - Canary Islands General Indirect Tax (Liable for IGIC tax)
        - Liable for IPSI (Ceuta/Melilla tax)""",
    )
    exemption_reason_code: Optional[str] = element(
        tag="ExemptionReason",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "extended"},
        description="""A code specifying a reason for exemption from this trade
        related tax, levy or duty.""",
        # TODO: find a specify a code list
    )
    rate_applicable_percent: Optional[float] = element(
        tag="RateApplicablePercent",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "comfort"},
        description="""The VAT rate, represented as percentage that applies to the
        item.""",
    )


class SpecifiedTradeSettlementLineMonetarySummation(
    BaseXmlModel,
    tag="SpecifiedTradeSettlementLineMonetarySummation",
    ns="ram",
    nsmap=RAM,
):
    """ram:SpecifiedLineTradeSettlement

    Profiles:
        - Factur-X: basic
        - Order-X: basic
    """

    line_total_amount: float = element(
        tag="LineTotalAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "basic"},
        description="""The total amount of the order line.""",
        usage="""The amount is “net” without VAT, i.e. inclusive of line level
        allowances and charges as well as other relevant taxes.""",
    )
    charge_total_amount: Optional[float] = element(
        tag="ChargeTotalAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "extended"},
        description="""The total amount of Charges of the order line.""",
        usage="""The amount is “net” without VAT, i.e. inclusive of line level
        allowances and charges as well as other relevant taxes.""",
    )
    allowance_total_amount: Optional[float] = element(
        tag="AllowanceTotalAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "extended"},
        description="""The total amount of Allowances of the order line.""",
        usage="""The amount is “net” without VAT, i.e. inclusive of line level
        allowances and charges as well as other relevant taxes.""",
    )
    tax_total_amount: Optional[float] = element(
        tag="TaxTotalAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "extended"},
        description="""The total amount of Taxes (VAT) of the order line.""",
    )
    total_allowance_charge_amount: Optional[float] = element(
        tag="TotalAllowanceChargeAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "extended"},
        description="""A monetary value of a total allowance and charge reported
        in this trade settlement line monetary summation.""",
        usage="""The amount is “net” without VAT, i.e. inclusive of line level
        allowances and charges as well as other relevant taxes.""",
    )


class SpecifiedLineTradeSettlement(
    BaseXmlModel,
    tag="SpecifiedLineTradeSettlement",
    ns="ram",
    nsmap=RAM,
):
    """ram:SpecifiedLineTradeSettlement

    Profiles:
        - Factur-X: basic
        - Order-X: basic
    """

    applicable_trade_tax: Optional[ApplicableTradeTax] = element(
        tag="ApplicableTradeTax",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "comfort"},
        description="""A group of business terms providing information about the
        VAT applicable for the goods and services ordered on the order line.""",
    )
    # specified_trade_allowance_charge # SpecifiedTradeAllowanceCharge
    specified_trade_settlement_line_monetary_summation: SpecifiedTradeSettlementLineMonetarySummation = element(
        tag="SpecifiedTradeSettlementLineMonetarySummation",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "basic"},
    )
    # receivable_specified_trade_accounting_account  # ReceivableSpecifiedTradeAccountingAccount


class IncludedSupplyChainTradeLineItem(
    BaseXmlModel,
    tag="IncludedSupplyChainTradeLineItem",
    ns="ram",
    nsmap=RAM,
):
    """ram:IncludedSupplyChainTradeLineItem

    level: 2

    Profiles:
        - Factur-X: basic
        - Order-X: basic
    """

    associated_document_line_document: AssociatedDocumentLineDocument = element(
        tag="AssociatedDocumentLineDocument",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "basic"},
    )
    specified_trade_product: SpecifiedTradeProduct = element(
        tag="SpecifiedTradeProduct",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "basic"},
        description="""A group of business terms providing information about the goods
        and services ordered or invoicedd.""",
        usage="""For order-x: An Order or a Change Order (Typecode BT-3 = 220 or 230) 
        MUST contain at least 1 Product in each line. 
        An order Response (BT-3 = 231) MUST contain a Product OR a Substituted Product

        In order-x can be 0 or 1, in factur-x must be 1.""",
    )
    # substituted_referenced_product # SubstitutedReferencedProduct
    specified_line_trade_agreement: SpecifiedLineTradeAgreement = element(
        tag="SpecifiedLineTradeAgreement",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "basic"},
        description="""A group of business terms providing information about the
        conditions of the goods and services ordered or invoiced.""",
    )
    specified_line_trade_delivery: SpecifiedLineTradeDelivery = element(
        tag="SpecifiedLineTradeDelivery",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "basic"},
    )
    specified_line_trade_settlement: SpecifiedLineTradeSettlement = element(
        tag="SpecifiedLineTradeSettlement",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic", "order-x": "basic"},
    )


class ApplicableTradeDeliveryTerms(
    BaseXmlModel,
    tag="ApplicableTradeDeliveryTerms",
    ns="ram",
    nsmap=RAM,
):
    """ram:ApplicableTradeDeliveryTerms

    Profiles:
        - Factur-X: extended
        - Order-X: basic
    """

    delivery_type_code: Optional[str] = element(
        tag="DeliveryTypeCode",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "basic"},
        description="""The code specifying the type of delivery for these
        trade delivery terms.""",
        usage="""To be chosen from the entries in UNTDID 4053 + INCOTERMS List 
        1 : Delivery arranged by the supplier (Indicates that the supplier will
            arrange delivery of the goods).
        2 : Delivery arranged by logistic service provider (Code indicating that the
            logistic service provider has arranged the delivery of goods).
        CFR : Cost and Freight (insert named port of destination)
        CIF : Cost, Insurance and Freight (insert named port of destination)
        CIP : Carriage and Insurance Paid to (insert named place of destination)   
        CPT : Carriage Paid To (insert named place of destination)
        DAP : Delivered At Place (insert named place of destination)
        DAT : Delivered At Terminal (insert named terminal at port or place of
              destination)
        DDP : Delivered Duty Paid (insert named place of destination)
        EXW : Ex Works (insert named place of delivery)
        FAS : Free Alongside Ship (insert named port of shipment)
        FCA : Free Carrier (insert named place of delivery)
        FOB : Free On Board (insert named port of shipment)""",
    )
    description: Optional[str] = element(
        tag="Description",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "comfort"},
        description="""A textual description of these trade delivery terms.""",
    )
    delivery_mode: Optional[str] = element(
        tag="FunctionCode",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "basic"},
        description="""A code specifying a function of these trade delivery terms
        (Pick up,or delivered).""",
        # TODO: get the list of codes
        usage="""To be chosen from the entries in UNTDID 4055""",
    )
    # relevant_trade_location # RelevantTradeLocation


class ApplicableHeaderTradeAgreement(
    BaseXmlModel,
    tag="ApplicableHeaderTradeAgreement",
    ns="ram",
    nsmap=RAM,
):
    """ram:ApplicableHeaderTradeAgreement

    level: 2

    Profiles:
        - Factur-X: minimum
        - Order-X: basic
    """

    buyer_reference: Optional[str] = element(
        tag="BuyerReference",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="""An identifier assigned by the Buyer used for internal
        routing purposes.""",
        usage="""The identifier is defined by the Buyer
        (e.g. contact ID, department, office id, project code).""",
    )
    seller_trade_party: TradeParty = element(
        tag="SellerTradeParty",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="""A group of business terms providing information about
        the Seller.""",
    )
    buyer_trade_party: TradeParty = element(
        tag="BuyerTradeParty",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="""A group of business terms providing information about
        the Buyer.""",
    )
    buyer_requisitioner_trade_party: Optional[TradeParty] = element(
        tag="BuyerRequisitionerTradeParty",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "comfort"},
        description="""The Party who raises the Order originally on
        behalf of the Buyer.""",
    )
    product_end_user_trade_party: Optional[TradeParty] = element(
        tag="ProductEndUserTradeParty",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "comfort"},
        description="""The Party who raise th Order originally on
        behalf of the Buyer.""",
    )
    applicable_trade_delivery_terms: Optional[ApplicableTradeDeliveryTerms] = element(
        tag="ApplicableTradeDeliveryTerms",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
    )
    seller_order_referenced_document: Optional[DocumentReference] = element(
        tag="SellerOrderReferencedDocument",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "comfort"},
    )
    buyer_order_referenced_document: Optional[DocumentReference] = element(
        tag="BuyerOrderReferencedDocument",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
    )
    quotation_reference: Optional[DocumentReference] = element(
        tag="QuotationReferencedDocument",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "basic"},
    )
    contract_reference: Optional[DocumentReference] = element(
        tag="ContractReferencedDocument",
        ns="ram",
        nsmap=RAM,
        profiles={"basic_wl": None, "order-x": "basic"},
    )
    requisition_reference: Optional[DocumentReference] = element(
        tag="RequisitionReferencedDocument",
        ns="ram",
        nsmap=RAM,
        profiles={"basic_wl": None, "order-x": "comfort"},
    )
    # additional_reference_document # AdditionalReferencedDocument
    buyer_agent: Optional[TradeParty] = element(
        tag="BuyerAgentTradeParty",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "comfort"},
        description="""The Party who raise th Order originally on behalf of the Buyer.""",
    )
    # catalogue_referenced_document # CatalogueReferencedDocument
    # blanket_order_referenced_document # BlanketOrderReferencedDocument
    # previous_order_referenced_document # PreviousOrderReferencedDocument
    # previous_order_change_referenced_document # PreviousOrderChangeReferencedDocument
    # previous_order_response_referenced_document # PreviousOrderResponseReferencedDocument
    # project_reference # SpecifiedProcuringProject
    # ultimate_customer_order_referenced_document # UltimateCustomerOrderReferencedDocument


class ApplicableHeaderTradeDelivery(
    BaseXmlModel,
    tag="ApplicableHeaderTradeDelivery",
    ns="ram",
    nsmap=RAM,
):
    """rsm:ApplicableHeaderTradeDelivery

    Profiles:
        - Factur-X: minimum
        - Order-X: basic
    """

    ship_to_party: Optional[TradeParty] = element(
        tag="ShipToTradeParty",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "comfort"},
        description="""A group of business terms providing information about where and
        when the goods and services ordered are delivered.""",
    )
    ultimate_ship_to_party: Optional[TradeParty] = element(
        tag="UltimateShipToTradeParty",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "comfort"},
        description="""A group of business terms providing information about where
        and when the goods and services ordered are delivered.""",
    )
    ship_from_party: Optional[TradeParty] = element(
        tag="ShipFromTradeParty",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "comfort"},
    )
    # requested_delivery_date # RequestedDeliverySupplyChainEvent
    # requested_pickup_date # RequestedDespatchSupplyChainEvent


class SpecifiedTradeSettlementHeaderMonetarySummation(
    BaseXmlModel,
    tag="SpecifiedTradeSettlementHeaderMonetarySummation",
    ns="ram",
    nsmap=RAM,
):
    """rsm:SpecifiedTradeSettlementHeaderMonetarySummation

    Profiles:
        - Factur-X: minimum
        - Order-X: basic
    """

    line_total_amount: float = element(
        tag="LineTotalAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""Sum of all line net amounts in the order.""",
    )
    charge_total_amount: Optional[float] = element(
        tag="ChargeTotalAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""Sum of all charges on document level in the order.""",
        usage="""Charges on line level are included in the order line net amount
        which is summed up into the Sum of order line net amount.""",
    )
    allowance_total_amount: Optional[float] = element(
        tag="AllowanceTotalAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""Sum of all allowances on document level in the order.""",
        usage="""Allowances on line level are included in the order line net amount
        which is summed up into the Sum of order line net amount.""",
    )
    tax_basis_total_amount: Optional[Amount] = element(
        tag="TaxBasisTotalAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="""The total amount of the order without VAT.""",
        usage="""The order total amount without VAT is the Sum of order line net
        amount minus Sum of allowances on document level
        plus Sum of charges on document level.""",
    )
    tax_total_amounts: Optional[List[Amount]] = element(
        tag="TaxTotalAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="""The total VAT amount for the order.""",
        usage="""The order total amount without VAT is the Sum of order line net
        amount minus Sum of allowances on document level
        plus Sum of charges on document level.""",
    )
    rounding_amount: Optional[float] = element(
        tag="RoundingAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""The amount to be added to the order total to round the
        amount to be paid.""",
    )
    grand_total_amount: Optional[Amount] = element(
        tag="GrandTotalAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="""The total amount of the order with VAT.""",
        usage="""The order total amount with VAT is the order total amount without VAT
        plus the order total VAT amount.""",
    )
    total_prepaid_amount: Optional[float] = element(
        tag="TotalPrepaidAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""The sum of amounts which have been paid in advance.""",
        usage="""This amount is subtracted from the total amount with VAT to
        calculate the amount due for payment.""",
    )
    due_payable_amount: Optional[float] = element(
        tag="DuePayableAmount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""The outstanding amount that is requested to be paid.""",
        usage="""This amount is the total amount with VAT minus the paid
        amount that has been paid in advance.
        The amount is zero in case of a fully paid Invoice.
        The amount may be negative; in that case the Seller owes the
        amount to the Buyer.""",
    )


class ReceivableSpecifiedTradeAccountingAccount(
    BaseXmlModel,
    tag="ReceivableSpecifiedTradeAccountingAccount",
    ns="ram",
    nsmap=RAM,
):
    """rsm:ReceivableSpecifiedTradeAccountingAccount

    Profiles:
        - Factur-X: basic_wl
        - Order-X: basic
    """

    reference_id: str = element(
        tag="ID",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""A textual value that specifies where to book the relevant data
        into the Buyer's financial accounts.""",
    )
    reference_type_code: Optional[str] = element(
        tag="TypeCode",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "extended"},
        description="""The code specifying the type of trade accounting account,
        such as general (main), secondary, cost accounting or budget account.""",
    )


class ApplicableHeaderTradeSettlement(
    BaseXmlModel,
    tag="ApplicableHeaderTradeSettlement",
    ns="ram",
    nsmap=RAM,
):
    """rsm:ApplicableHeaderTradeSettlement

    Profiles:
        - Factur-X: minimum
        - Order-X: basic
    """

    tax_currency_code: Optional[str] = element(
        tag="TaxCurrencyCode",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "extended"},
        description="""The currency in which all order amounts are given""",
        usage="""Only one currency shall be used in the order""",
    )
    order_currency_code: Optional[str] = element(
        tag="OrderCurrencyCode",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "basic"},
        description="""The currency in which all order amounts are given""",
        usage="""Only one currency shall be used in the order""",
    )
    invoice_currency_code: Optional[str] = element(
        tag="InvoiceCurrencyCode",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "extended"},
        description="""The currency in which all invoice amounts must be given, except
        for the Total VAT amount in accounting currency.""",
    )
    invoicer_party: Optional[TradeParty] = element(
        tag="InvoicerTradeParty",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "extended"},
        description="""The Party who should issue or send the invoice on behalf
        of the supplier.""",
    )
    invoicee_party: Optional[TradeParty] = element(
        tag="InvoicerTradeParty",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "comfort"},
        description="""The Party to which the invoice must be sent.""",
    )
    # specified_trade_settlement_payment_means # SpecifiedTradeSettlementPaymentMeans
    # applicable_trade_tax # ApplicableTradeTax
    # specified_trade_allowance_charge # SpecifiedTradeAllowanceCharge
    # specified_trade_allowance_charge # SpecifiedTradeAllowanceCharge
    # specified_logistics_service_charge # SpecifiedLogisticsServiceCharge
    # specified_trade_payment_terms # SpecifiedTradePaymentTerms
    total_amounts: SpecifiedTradeSettlementHeaderMonetarySummation = element(
        tag="SpecifiedTradeSettlementHeaderMonetarySummation",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="""A group of business terms providing the monetary totals
        for the order.""",
    )
    receivable_specified_trade_accounting_account: Optional[
        ReceivableSpecifiedTradeAccountingAccount
    ] = element(
        tag="ReceivableSpecifiedTradeAccountingAccount",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
    )


class SupplyChainTradeTransaction(
    BaseXmlModel,
    tag="SupplyChainTradeTransaction",
    ns="rsm",
    nsmap=RSM,
):
    """rsm:SupplyChainTradeTransaction

    Profiles:
        - Factur-X: minimum
        - Order-X: basic
    """

    included_supply_chain_trade_line_items: List[
        IncludedSupplyChainTradeLineItem
    ] = element(
        tag="IncludedSupplyChainTradeLineItem",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "basic"},
        description="""A group of business terms providing information on 
        individual lines.""",
        usage="""At least one line mandatory in invoices, zero line mandatory in orders.
        Currently, at least one line in orders too.""",
    )
    applicable_header_trade_agreement: ApplicableHeaderTradeAgreement = element(
        tag="ApplicableHeaderTradeAgreement",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
    )
    applicable_header_trade_delivery: ApplicableHeaderTradeDelivery = element(
        tag="ApplicableHeaderTradeDelivery",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
    )
    header_trade_settlement: ApplicableHeaderTradeSettlement = element(
        tag="ApplicableHeaderTradeSettlement",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
    )
