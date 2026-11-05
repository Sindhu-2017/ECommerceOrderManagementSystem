import asyncio
import logging
import smtplib
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

from app.core.config import get_settings
from app.models.order import Order

logger = logging.getLogger(__name__)


class EmailService:
    async def send_order_confirmation(self, receiver: str, order: Order) -> bool:
        return await asyncio.to_thread(
            self._send_order_confirmation_sync, receiver, order
        )

    def _send_order_confirmation_sync(self, receiver: str, order: Order) -> bool:
        settings = get_settings()

        sender = settings.EMAIL_SENDER
        password = settings.EMAIL_PASSWORD.get_secret_value()

        if not sender or not password:
            logger.error("Gmail SMTP credentials are not configured.")
            return False

        message = EmailMessage()
        message["Subject"] = (
            f"Order Management - Order #{order.order_id} Created Successfully"
        )
        message["From"] = sender
        message["To"] = receiver
        message["Date"] = formatdate(localtime=True)
        message["Message-ID"] = make_msgid()

        item_details = ""

        for item in order.items:
            item_details += f"""
            Product ID   : {item.product_id}
            Quantity     : {item.quantity}
            Unit Price   : ₹{item.unit_price}
            Subtotal     : ₹{item.subtotal}
            """

        email_body = f"""
Hello,

Your order has been created successfully.

Order Details
-------------
Order ID       : {order.order_id}
Order Date     : {order.order_date}
Order Status   : {order.order_status}

Ordered Products
----------------
{item_details}

Total Amount   : ₹{order.total_amount}

Shipping Details
----------------
Recipient Name : {order.shipping_recipient_name}
Phone          : {order.shipping_phone}
Address        : {order.shipping_address_line}
City           : {order.shipping_city}
State          : {order.shipping_state}
Pincode        : {order.shipping_pincode}

Thank you for shopping with us.

Regards,
E-Commerce Team
"""

        message.set_content(email_body)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as smtp:
                # authenticate Gmail account
                smtp.login(sender, password)

                # send order confirmation email
                smtp.send_message(message)

            logger.info(
                "Order confirmation email sent successfully for order_id=%s",
                order.order_id,
            )
            return True

        except (smtplib.SMTPException, OSError):
            logger.exception(
                "Failed to send order confirmation email for order_id=%s",
                order.order_id,
            )
            return False
