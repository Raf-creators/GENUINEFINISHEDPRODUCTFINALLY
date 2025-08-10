# PNM Gardeners - Email Notification Setup Guide

## 📧 Current Email Configuration

The PNM Gardeners website is configured to send email notifications to:
**📫 gardeningpnm@gmail.com**

## ✅ What's Already Implemented

### 1. Email Service (`backend/email_service.py`)
- Professional HTML email templates
- Quote request notifications 
- Contact form notifications
- Customer confirmation emails
- Automatic email logging to backend server logs

### 2. Form Submissions Trigger Emails
- **Quote Request Form**: Sends notification to gardeningpnm@gmail.com + confirmation to customer
- **Contact Form**: Sends notification to gardeningpnm@gmail.com + confirmation to customer

### 3. Admin Dashboard
- View all form submissions at: `http://localhost:3000/admin`
- Track quote requests and contact form submissions
- Customer details and messages displayed professionally

## 📨 Email Templates Include

### Business Notification Emails:
- Customer contact details (name, email, phone)
- Service requested
- Customer message
- Timestamp of submission
- Professional PNM Gardeners branding

### Customer Confirmation Emails:
- Thank you message
- Response timeline (24 hours)
- Contact information
- Professional branding with logo

## 🔧 To Enable Actual Email Sending

Currently, email content is logged to the backend server logs. To enable actual email delivery:

### Option 1: Gmail SMTP (Recommended)
1. Enable 2-factor authentication on gardeningpnm@gmail.com
2. Generate an App Password in Google Account settings
3. Update backend environment variables:
   ```bash
   SMTP_EMAIL=gardeningpnm@gmail.com
   SMTP_PASSWORD=your_app_password
   ```

### Option 2: Professional Email Service (SendGrid, Mailgun)
1. Sign up for a service like SendGrid
2. Get API key
3. Update email service configuration

## 🚀 Current Status

✅ **Form Data Collection**: All submissions stored in MongoDB
✅ **Email Templates**: Professional HTML emails ready
✅ **Admin Dashboard**: Full management interface at /admin
✅ **Error Handling**: Graceful fallbacks if email fails
✅ **Customer Experience**: Confirmation messages and smooth UX

📧 **Email Notifications**: Logged to server (ready for SMTP setup)

## 📋 Form Submissions Go To:

1. **MongoDB Database**: Permanently stored with full details
2. **Backend Server Logs**: Email content logged for review
3. **Admin Dashboard**: Visual interface to manage leads
4. **Email Notifications**: Ready to send to gardeningpnm@gmail.com

## 🎯 Next Steps

1. **Access Admin Dashboard**: Visit http://localhost:3000/admin to see all submissions
2. **Check Server Logs**: View backend logs to see email notifications
3. **Optional**: Configure SMTP to enable actual email delivery
4. **Test**: Submit forms to verify everything works

## 📞 Contact Information

All forms will collect:
- Customer name
- Email address  
- Phone number
- Service requested
- Custom message
- Submission timestamp

This data flows to gardeningpnm@gmail.com notifications and the admin dashboard for easy customer management!