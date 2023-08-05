"""Pydantic XML models for Factur-X and Order-X schemas."""
from pydantic_xml import BaseXmlModel, element


from .document_context import ExchangedDocumentContext
from .exchanged_document import ExchangedDocument
from .supply_chain_trade_transaction import SupplyChainTradeTransaction


class SCRDMCCBDACIOMessageStructure(
    BaseXmlModel,
    tag="SCRDMCCBDACIOMessageStructure",
    ns="rsm",
    nsmap={
        "rsm": "urn:un:unece:uncefact:data:SCRDMCCBDACIOMessageStructure:100",
        "udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:128",
        "qtd": "urn:un:unece:uncefact:data:standard:QualifiedDataType:128",
        "ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:128",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    },
):
    """Root Factur-X and Order-X element.

    nsmaps are fully definied here.
    """

    exchanged_document_context: ExchangedDocumentContext = element(
        ns="rsm",
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="""A group of business terms providing information on the business
        process and rules applicable to the Invoice document.""",
    )
    exchanged_document: ExchangedDocument = element(
        ns="rsm",
        profiles={"factur-x": "minimum", "order-x": "basic"},
    )
    supply_chain_trade_transaction: SupplyChainTradeTransaction = element(
        ns="rsm",
        profiles={"factur-x": "minimum", "order-x": "basic"},
    )


# Alias for the root element
Root = SCRDMCCBDACIOMessageStructure
