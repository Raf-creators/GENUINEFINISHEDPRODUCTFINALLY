import React, { useState, useEffect } from "react";
import { apiService } from "../services/api";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Mail, Phone, Calendar, User, MessageSquare, Star } from "lucide-react";

const AdminDashboard = () => {
  const [quotes, setQuotes] = useState([]);
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [quotesData, contactsData] = await Promise.all([
          apiService.getQuoteRequests(),
          apiService.getContacts()
        ]);
        setQuotes(quotesData);
        setContacts(contactsData);
      } catch (error) {
        console.error('Error fetching admin data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-xl text-gray-600">Loading admin dashboard...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">PNM Gardeners - Admin Dashboard</h1>
          <p className="text-gray-600">Manage your quote requests and contact form submissions</p>
        </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Quote Requests</p>
                  <p className="text-3xl font-bold text-green-700">{quotes.length}</p>
                </div>
                <MessageSquare className="w-8 h-8 text-green-700" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Contact Forms</p>
                  <p className="text-3xl font-bold text-blue-700">{contacts.length}</p>
                </div>
                <Mail className="w-8 h-8 text-blue-700" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Inquiries</p>
                  <p className="text-3xl font-bold text-purple-700">{quotes.length + contacts.length}</p>
                </div>
                <User className="w-8 h-8 text-purple-700" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quote Requests */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Quote Requests</h2>
          <div className="space-y-4">
            {quotes.length === 0 ? (
              <Card>
                <CardContent className="p-6 text-center text-gray-500">
                  No quote requests yet.
                </CardContent>
              </Card>
            ) : (
              quotes.map((quote) => (
                <Card key={quote.id} className="hover:shadow-md transition-shadow">
                  <CardHeader className="pb-3">
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-lg font-semibold text-gray-900">
                          {quote.name}
                        </CardTitle>
                        <div className="flex items-center space-x-2 mt-1">
                          <Badge variant="outline" className="text-green-700 border-green-200">
                            {quote.service}
                          </Badge>
                          <Badge variant={quote.status === 'pending' ? 'destructive' : 'default'}>
                            {quote.status}
                          </Badge>
                        </div>
                      </div>
                      <div className="text-sm text-gray-500">
                        <Calendar className="w-4 h-4 inline mr-1" />
                        {formatDate(quote.created_at)}
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="space-y-3">
                      <div className="flex items-center space-x-4 text-sm">
                        <div className="flex items-center space-x-1">
                          <Mail className="w-4 h-4 text-gray-500" />
                          <span>{quote.email}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Phone className="w-4 h-4 text-gray-500" />
                          <span>{quote.phone}</span>
                        </div>
                      </div>
                      {quote.message && (
                        <div className="bg-gray-50 p-3 rounded-lg">
                          <p className="text-sm text-gray-700">{quote.message}</p>
                        </div>
                      )}
                      <div className="flex space-x-2">
                        <Button size="sm" className="bg-green-700 hover:bg-green-800">
                          <Phone className="w-4 h-4 mr-1" />
                          Call Customer
                        </Button>
                        <Button size="sm" variant="outline">
                          <Mail className="w-4 h-4 mr-1" />
                          Send Email
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </div>

        {/* Contact Forms */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Contact Form Submissions</h2>
          <div className="space-y-4">
            {contacts.length === 0 ? (
              <Card>
                <CardContent className="p-6 text-center text-gray-500">
                  No contact form submissions yet.
                </CardContent>
              </Card>
            ) : (
              contacts.map((contact) => (
                <Card key={contact.id} className="hover:shadow-md transition-shadow">
                  <CardHeader className="pb-3">
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-lg font-semibold text-gray-900">
                          {contact.name}
                        </CardTitle>
                        <div className="flex items-center space-x-2 mt-1">
                          <Badge variant="outline" className="text-blue-700 border-blue-200">
                            {contact.subject}
                          </Badge>
                          <Badge variant={contact.status === 'new' ? 'destructive' : 'default'}>
                            {contact.status}
                          </Badge>
                        </div>
                      </div>
                      <div className="text-sm text-gray-500">
                        <Calendar className="w-4 h-4 inline mr-1" />
                        {formatDate(contact.created_at)}
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="space-y-3">
                      <div className="flex items-center space-x-4 text-sm">
                        <div className="flex items-center space-x-1">
                          <Mail className="w-4 h-4 text-gray-500" />
                          <span>{contact.email}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Phone className="w-4 h-4 text-gray-500" />
                          <span>{contact.phone}</span>
                        </div>
                      </div>
                      {contact.message && (
                        <div className="bg-gray-50 p-3 rounded-lg">
                          <p className="text-sm text-gray-700">{contact.message}</p>
                        </div>
                      )}
                      <div className="flex space-x-2">
                        <Button size="sm" className="bg-blue-700 hover:bg-blue-800">
                          <Phone className="w-4 h-4 mr-1" />
                          Call Customer
                        </Button>
                        <Button size="sm" variant="outline">
                          <Mail className="w-4 h-4 mr-1" />
                          Send Email
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </div>

        {/* Email Notification Info */}
        <div className="mt-8 bg-green-50 border border-green-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-green-800 mb-2">📧 Email Notifications</h3>
          <p className="text-green-700 mb-2">
            All form submissions are automatically logged to the backend server logs and can be configured to send email notifications to:
          </p>
          <p className="font-semibold text-green-800">📫 contact@pnmgardening.com</p>
          <p className="text-sm text-green-600 mt-2">
            To enable actual email sending, you'll need to configure SMTP settings in the backend email service.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;