import logging

from app.agents.analyzer import SalesOrderAnalyzer
from app.erpnext.sales_order import SalesOrderService


logger = logging.getLogger(__name__)


def test_sales_order_analyzer_with_draft_order() -> None:
    # Arrange
    customer: str = "sandeep"

    analyzer: SalesOrderAnalyzer = SalesOrderAnalyzer()
    sales_order_service: SalesOrderService = SalesOrderService()

    orders: dict = {
        "data": [
            {
                "name": "SAL-ORD-2026-00001",
                "customer": "sandeep",
                "transaction_date": "2026-09-19",
                "status": "Draft",
            }
        ]
    }

    # Act
    order_counts: dict = sales_order_service.get_order_counts(orders)

    logger.info("Order counts: %s", order_counts)

    analysis: str = analyzer.analyze(
        customer=customer,
        orders=orders,
        order_counts=order_counts,
    )

    logger.info("Analyzer result: %s", analysis)

    # Assert
    assert order_counts["total"] == 1
    assert order_counts["draft"] == 1
    assert order_counts["completed"] == 0
    assert order_counts["cancelled"] == 0
    assert analysis