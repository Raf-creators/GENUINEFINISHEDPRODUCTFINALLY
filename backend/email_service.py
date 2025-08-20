import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # SendGrid configuration
        self.sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
        self.sender_email = os.environ.get('SENDER_EMAIL', 'gardeningpnm@gmail.com')
        self.business_email = "gardeningpnm@gmail.com"
        
        if not self.sendgrid_api_key:
            logger.warning("SENDGRID_API_KEY not found in environment variables")
        
    def send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send email using SendGrid"""
        try:
            message = Mail(
                from_email=self.sender_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content
            )

            sg = SendGridAPIClient(api_key=self.sendgrid_api_key)
            response = sg.send(message)
            
            if response.status_code == 202:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email. Status code: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
        
    async def send_quote_notification(self, quote_data):
        """Send email notification for new quote requests"""
        try:
            subject = f"New Quote Request - {quote_data.service}"
            
            # Create email content
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #2d5016; text-align: center;">New Quote Request - PNM Gardeners</h2>
                    
                    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #2d5016; margin-top: 0;">Customer Details:</h3>
                        <p><strong>Name:</strong> {quote_data.name}</p>
                        <p><strong>Email:</strong> {quote_data.email}</p>
                        <p><strong>Phone:</strong> {quote_data.phone}</p>
                        <p><strong>Service Requested:</strong> {quote_data.service}</p>
                    </div>
                    
                    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #2d5016; margin-top: 0;">Message:</h3>
                        <p style="background-color: white; padding: 15px; border-left: 4px solid #2d5016;">
                            {quote_data.message}
                        </p>
                    </div>
                    
                    <div style="background-color: #2d5016; color: white; padding: 15px; border-radius: 5px; text-align: center; margin: 20px 0;">
                        <p style="margin: 0;"><strong>Received:</strong> {datetime.now().strftime("%d %B %Y at %H:%M")}</p>
                    </div>
                    
                    <p style="text-align: center; color: #666; font-size: 14px; margin-top: 30px;">
                        This quote request was submitted through your PNM Gardeners website.
                    </p>
                </div>
            </body>
            </html>
            """
            
            # Send to business email
            success = self.send_email(self.business_email, subject, html_content)
            
            if success:
                logger.info(f"Quote notification sent to {self.business_email}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to send quote notification email: {e}")
            return False

    async def send_contact_notification(self, contact_data):
        """Send email notification for general contact form submissions"""
        try:
            subject = f"New Contact Form Submission - {contact_data.subject}"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #2d5016; text-align: center;">New Contact Form Submission - PNM Gardeners</h2>
                    
                    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #2d5016; margin-top: 0;">Contact Details:</h3>
                        <p><strong>Name:</strong> {contact_data.name}</p>
                        <p><strong>Email:</strong> {contact_data.email}</p>
                        <p><strong>Phone:</strong> {contact_data.phone}</p>
                        <p><strong>Subject:</strong> {contact_data.subject}</p>
                    </div>
                    
                    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #2d5016; margin-top: 0;">Message:</h3>
                        <p style="background-color: white; padding: 15px; border-left: 4px solid #2d5016;">
                            {contact_data.message}
                        </p>
                    </div>
                    
                    <div style="background-color: #2d5016; color: white; padding: 15px; border-radius: 5px; text-align: center; margin: 20px 0;">
                        <p style="margin: 0;"><strong>Received:</strong> {datetime.now().strftime("%d %B %Y at %H:%M")}</p>
                    </div>
                    
                    <p style="text-align: center; color: #666; font-size: 14px; margin-top: 30px;">
                        This message was submitted through your PNM Gardeners website contact form.
                    </p>
                </div>
            </body>
            </html>
            """
            
            # Send to business email  
            success = self.send_email(self.business_email, subject, html_content)
            
            if success:
                logger.info(f"Contact notification sent to {self.business_email}")
                
            return success
            
        except Exception as e:
            logger.error(f"Failed to send contact notification email: {e}")
            return False

    async def send_customer_confirmation(self, customer_email, customer_name, submission_type="quote"):
        """Send confirmation email to the customer"""
        try:
            if submission_type == "quote":
                subject = "Thank you for your quote request - PNM Gardeners"
                service_type = "quote request"
            else:
                subject = "Thank you for contacting us - PNM Gardeners"
                service_type = "message"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #2d5016;">PNM Gardeners</h1>
                        <p style="color: #666;">Professional Gardening Services in Balham, London</p>
                    </div>
                    
                    <h2 style="color: #2d5016;">Hello {customer_name},</h2>
                    
                    <p>Thank you for your {service_type}! We've received your submission and will get back to you within 24 hours.</p>
                    
                    <div style="background-color: #f0f8e8; padding: 20px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #2d5016;">
                        <h3 style="color: #2d5016; margin-top: 0;">What happens next?</h3>
                        <ul style="margin: 0; padding-left: 20px;">
                            <li>We'll review your request within 2-4 hours</li>
                            <li>One of our gardening specialists will contact you</li>
                            <li>We'll arrange a convenient time for a free consultation</li>
                            <li>You'll receive a detailed, competitive quote</li>
                        </ul>
                    </div>
                    
                    <div style="background-color: #2d5016; color: white; padding: 20px; border-radius: 5px; text-align: center; margin: 30px 0;">
                        <h3 style="margin-top: 0; color: white;">Need immediate assistance?</h3>
                        <p style="margin: 10px 0;">📞 <strong>Call us: 07748 853590</strong></p>
                        <p style="margin: 10px 0;">📧 <strong>Email: gardeningpnm@gmail.com</strong></p>
                        <p style="margin-bottom: 0; font-size: 14px;">Available 7 days a week, 8am - 6pm</p>
                    </div>
                    
                    <p style="text-align: center; color: #666; font-size: 14px; margin-top: 30px;">
                        Thank you for choosing PNM Gardeners - Your trusted gardening experts in Balham!
                    </p>
                </div>
            </body>
            </html>
            """
            
            # Send to customer
            success = self.send_email(customer_email, subject, html_content)
            
            if success:
                logger.info(f"Customer confirmation sent to {customer_email}")
                
            return success
            
        except Exception as e:
            logger.error(f"Failed to send customer confirmation email: {e}")
            return False

# Global email service instance
email_service = EmailService()