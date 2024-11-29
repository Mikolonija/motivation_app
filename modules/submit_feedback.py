import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import config
from utils.helpers import get_non_empty_input, msg_output


class FeedbackHandler:
    def __init__(self, message_body: str):
        self.message_body: str = message_body

    @classmethod
    def create_feedback_message(cls) -> str:
        print("\nAttention: To stop the action and back to menu, you can press (ctrl + C) or type (ctrl + Z) and press Enter")
        while True:
            message: str = get_non_empty_input("Write feedback: ", "Error: feedback cannot be empty")
            if not os.getenv("GMAIL_USER") or not os.getenv("GMAIL_PASSWORD"):
                msg_output("GMAIL_USER or GMAIL_PASSWORD is not set in environment variables.")
            else:
                return cls(message)

    def confirm_and_send(self) -> None:
        confirmation: str = self.confirm_send_decision()
        self.process_confirmation(confirmation)
        send_feedback()

    def confirm_send_decision(self) -> str:
        while True:
            confirm: str = get_non_empty_input("Do you want to send feedback? (yes/no): ", "Error: Input cannot be empty").lower()
            return confirm

    def process_confirmation(self, confirmation: str) -> None:
        os.system("cls")
        if confirmation == "yes":
            self.send_message()
        else:
            msg_output("Feedback email was not sent.")

    def send_message(self) -> None:
        try:
            subject = "Feedback Received"
            msg = MIMEMultipart()
            msg["From"] = os.getenv("GMAIL_USER")
            msg["To"] = os.getenv("GMAIL_USER")
            msg["Subject"] = subject
            msg.attach(MIMEText(self.message_body, "plain"))
            with smtplib.SMTP(config.smtp_server, config.smtp_host) as server:
                server.starttls()
                server.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASSWORD"))
                server.sendmail(os.getenv("GMAIL_USER"), os.getenv("GMAIL_USER"), msg.as_string())
            msg_output("Feedback email sent successfully.")
        except Exception as e:
            msg_output(f"Error sending email: {e}")


def send_feedback() -> None:
    feedback_handler: str = FeedbackHandler.create_feedback_message()
    if feedback_handler:
        feedback_handler.confirm_and_send()
    return None
