"""
Email sending utility using Brevo HTTP API (not SMTP).
Railway blocks SMTP ports, so we use the HTTP API instead.
"""
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from flask import current_app, url_for


def send_verification_email(user_email, token):
    """
    Send verification email via Brevo HTTP API.
    
    Args:
        user_email: The recipient's email address
        token: The verification token
    
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Configure Brevo API
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = current_app.config['BREVO_API_KEY']
        
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        
        # Generate verification URL
        verification_url = f"{current_app.config['APP_URL']}/verify/{token}"
        
        # Create email content
        sender = {
            "name": current_app.config['SENDER_NAME'],
            "email": current_app.config['SENDER_EMAIL']
        }
        
        to = [{"email": user_email}]
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 40px auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 30px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; }}
                .content {{ padding: 40px 30px; }}
                .button {{ 
                    display: inline-block; 
                    padding: 15px 35px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #ffffff !important; 
                    text-decoration: none; 
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 16px;
                    margin: 20px 0;
                }}
                .footer {{ 
                    background: #f8f9fa; 
                    padding: 30px; 
                    text-align: center; 
                    font-size: 13px; 
                    color: #666; 
                    border-top: 1px solid #eee;
                }}
                .link {{ color: #667eea; word-break: break-all; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 BBA Services</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">Email Verification</p>
                </div>
                <div class="content">
                    <h2 style="color: #333; margin-bottom: 20px;">Welcome to BBA Services!</h2>
                    <p style="margin-bottom: 20px;">Thank you for creating an account. To complete your registration and access your dashboard, please verify your email address by clicking the button below:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{verification_url}" class="button">Verify My Email</a>
                    </div>
                    
                    <p style="margin-bottom: 15px;">Or copy and paste this link into your browser:</p>
                    <p style="background: #f8f9fa; padding: 15px; border-radius: 6px; border-left: 4px solid #667eea;">
                        <a href="{verification_url}" class="link">{verification_url}</a>
                    </p>
                    
                    <p style="margin-top: 30px; color: #666; font-size: 14px;">
                        <strong>Security Note:</strong> This verification link will expire in 24 hours for your security.
                    </p>
                </div>
                <div class="footer">
                    <p style="margin: 0 0 10px 0;"><strong>BBA Services</strong></p>
                    <p style="margin: 0 0 5px 0;">This is an automated message from noreply@bbaservices.org</p>
                    <p style="margin: 0;">If you didn't create an account, please ignore this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        subject = "Verify Your Email - BBA Services"
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            html_content=html_content,
            sender=sender,
            subject=subject
        )
        
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Verification email sent successfully to {user_email}")
        return True
        
    except Exception as e:
        print(f"Failed to send email to {user_email}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        import traceback
        traceback.print_exc()
        return False
