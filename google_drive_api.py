# Real Google Drive Photo API Integration
# This will fetch ALL actual photos from your Google Drive folders

import json
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from typing import Dict, List, Any

class RealGoogleDriveAPI:
    def __init__(self):
        # Your service account credentials
        self.credentials_json = {
            "type": "service_account",
            "project_id": "neon-fiber-468814-d9",
            "private_key_id": "3d36ab1746747fda626a5f0bb96e956ee0ea1e9b",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDIFvcBHrEEzk93\n6K5IM1ygp+kau5mryGIiV+NBRhmSdwfAdJjQ3oFW8tlW/cKy2go/nHMZJD385Ahu\nDyJYpSLU1m1RjYAL+9Os0jWVnpO5whMFYv4jFfZ+N4ZThTiWeGgGwac7QmdrBzBr\naIctQvdoi8oYQ5KJn5ITjBdOK/pe0x/grORQIDQOo0n0l+RbTNTH1OI5yWOCPDKh\nGzRdnqfzGdUt5hPolcRzAjWWjPtRTfqJ9kmGCPP8l2PQOXfbzQEGqTnrsWugKSQt\nnBkyHOg/BZeJby42wZzMVRkEtPoUnDkQA2q1bLlcGiiwo6eI2hNKV8TKzm4s4gQL\nHF2OyIeJAgMBAAECggEAAxLdPQJqcDs2G86yfK/zTJF/wnYezHWB0mq8tjg8NNSI\nxTNVVKISZRJKdexkhQhV73e5CeoVXLDpEz2+xpNU12Wq3L2aebSm4gkBoziCJvCd\nB7BnXIUeGf7C3L4XajJT0MTBS6b/vTRpUUEUEIUulUfOdTR2iBAwN4Ynpn8E89dt\n8mupcseT8LsrCl+s3QXbeOrakDcE1/qUeokx85EkYW5z5FkVVBFwL3elZukKm1AQ\n4euRU680fOG0FBSzBMsk6wMUxOiPGUiAgrT8PWxZw9D0QtISLYQjdLLBF8dfkau0\nDB+fBAmPsAMiEZdzROaANcEuTssJi78OxTFMc3mG/QKBgQD4UtlWHtezH2Rgrf2E\nRTFhnizzxhrIPv5qHueQYbMbsQQj2HQrssY4n2JsXT4xFZroeNKoVQk0SKMXaEwM\ndp4Vm1L+glI4zH+OjE3vrSTV86LpXENqsSVGi1gDxyzayq0c7cncxIwx3I6RsGdj\nsToXv+aV5GHRf3f3ZdkVmxTcJQKBgQDORmiZVREkGyVJYmRoLE0JT5alIx3nfBfX\nm+db0/lK43hWCHeFINP+yW6diUtaUmn6W8i5WQpijK6yz1mnyheplWvGURFizKTe\nfibTRuaa7fGx/AKBtDD5CXASf5cp5NnCGQcbeRcEFBet9Nn0zE3ibcylVttkufmW\nmCZR3PLulQKBgQCCV/p8mfPesbueg7VumGMzOjOeQX4NXgNs8Ivb3WyGPIRPzG4u\nAcjKL98ZwlfCq/SD0efBM+GA8B+rSbOhVyHjdYQ6020VI0JRMJQ4Gkobg6cflq5M\ncm9+d+XbFdEVhw0XAjnTB9gO1BaBonaifYRgsvn188rkjGQMGAm6rYxlgQKBgQCo\nwRFx4BZV459tmgFq+FNN+r7T+xbL+snGqtVsWs7oZZBdUi/1yhWlrEXCvD/ZdPMe\nz1g3ypCkb1O9FcXTb5JMOuIhLNF8cs+u9qXs02R1+5RweCvU0QX/t6joeVnB/Gfq\nU29tGnOp8oYs2tQ1Ya+WPx3dZmG21i9K9M7kyk40wQKBgQCN1xCAoi98KVItY110\nTZ23VbNCHIGiflhCukFAWgBaBUCO6su2ZEGAu6NwBNwXAAwATYnko8vXHNHCaZlR\nYkYCg6fVbAFUMknvto2pnqdgWSWfICwYh3QcG0cm4bXhIy73XsQ17tHdotVoUg0o\neOqGcadDn4EB2KG42Ljrn06aGA==\n-----END PRIVATE KEY-----\n",
            "client_email": "pnm-photo-access@neon-fiber-468814-d9.iam.gserviceaccount.com",
            "client_id": "115553813467939254982",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pnm-photo-access%40neon-fiber-468814-d9.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }
        
        # Your Google Drive folder IDs
        self.service_folders = {
            "Trellis": "1ZNS3E2qnlSBWpgfo5au0BMAI6wVWgkMF",
            "Planting": "1HrLDmVwtZgNOtmSodwBsCJzQxXNmqjcw", 
            "Patio": "18FYoofEdGLDF6ecLbjrXY4YxNVdmaJZB",
            "Garden Clearance": "1h0Kk1XM89ZQo-gmDpCNNz2jC8efXs1DF",
            "Hedge Trimming": "1vMJJAExNv9zvBwzp0p5WX9etf4NJNjfY",
            "Lawn Care": "1VElZ2qjL_Yu-I9tHCRgxWe7qD7IcFXrn",
            "Maintenance": "1T8eB6pCzjPebDSNvcuyePmYmKFnxpaC_",
            "Tree Services": "1iogjSXnisXibFs5xpdMJNI8wC-ywA7uU",
            "General": "1oRHb8w7XCDnZRq7hHSIfXPHe8dedi4ab"
        }
        
        self.service = None
        
    def authenticate(self):
        """Authenticate with Google Drive API"""
        try:
            # Create credentials from the JSON
            credentials = service_account.Credentials.from_service_account_info(
                self.credentials_json,
                scopes=['https://www.googleapis.com/auth/drive.readonly']
            )
            
            # Build the Drive API service
            self.service = build('drive', 'v3', credentials=credentials)
            print("✅ Successfully authenticated with Google Drive API")
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {str(e)}")
            return False
    
    def get_folder_files(self, folder_id: str, service_name: str) -> List[Dict[str, Any]]:
        """Get all image files from a specific folder"""
        if not self.service:
            print("❌ Not authenticated. Call authenticate() first.")
            return []
        
        try:
            print(f"🔍 Fetching photos from {service_name} folder...")
            
            # Query for image files in the folder
            query = f"parents in '{folder_id}' and (mimeType contains 'image/' or name contains '.jpg' or name contains '.jpeg' or name contains '.png' or name contains '.heic')"
            
            results = self.service.files().list(
                q=query,
                fields="files(id, name, mimeType, size, createdTime, webViewLink)",
                pageSize=1000  # Get up to 1000 files
            ).execute()
            
            files = results.get('files', [])
            
            # Convert to our photo format
            photos = []
            for file in files:
                photo = {
                    'id': file['id'],
                    'name': file['name'],
                    'service': service_name,
                    'url': f"https://drive.google.com/file/d/{file['id']}/view",
                    'direct_url': f"https://drive.google.com/uc?export=view&id={file['id']}",
                    'thumbnail_url': f"https://drive.google.com/thumbnail?id={file['id']}&sz=w400",
                    'download_url': f"https://drive.google.com/uc?export=download&id={file['id']}",
                    'size': file.get('size', 0),
                    'created': file.get('createdTime', ''),
                    'mime_type': file.get('mimeType', ''),
                    'web_link': file.get('webViewLink', '')
                }
                photos.append(photo)
            
            print(f"✅ Found {len(photos)} photos in {service_name}")
            return photos
            
        except Exception as e:
            print(f"❌ Error fetching {service_name} photos: {str(e)}")
            return []
    
    def get_all_service_albums(self) -> Dict[str, Dict[str, Any]]:
        """Get all photos organized by service albums"""
        
        if not self.authenticate():
            print("❌ Failed to authenticate with Google Drive")
            return {}
        
        print("🚀 FETCHING ALL REAL PHOTOS FROM GOOGLE DRIVE")
        print("="*60)
        
        service_albums = {}
        total_photos = 0
        
        for service_name, folder_id in self.service_folders.items():
            photos = self.get_folder_files(folder_id, service_name)
            
            if photos:
                # Create service album
                service_albums[service_name] = {
                    'service_name': service_name,
                    'folder_id': folder_id,
                    'photo_count': len(photos),
                    'photos': photos,
                    'description': self.get_service_description(service_name),
                    'cover_photo': photos[0]['direct_url'] if photos else None
                }
                total_photos += len(photos)
            else:
                print(f"⚠️ No photos found in {service_name} folder")
                service_albums[service_name] = {
                    'service_name': service_name,
                    'folder_id': folder_id,
                    'photo_count': 0,
                    'photos': [],
                    'description': self.get_service_description(service_name),
                    'cover_photo': None
                }
        
        print(f"\n🎉 GOOGLE DRIVE INTEGRATION COMPLETE!")
        print(f"📸 Total photos found: {total_photos}")
        print(f"📁 Service albums: {len(service_albums)}")
        
        # Show breakdown
        print(f"\n📊 PHOTOS BY SERVICE:")
        for service_name, album in service_albums.items():
            print(f"   {service_name}: {album['photo_count']} photos")
        
        return service_albums
    
    def get_service_description(self, service_name: str) -> str:
        """Get description for each service"""
        descriptions = {
            'Trellis': 'Custom trellis installation and wooden fencing solutions for privacy and garden structure.',
            'Planting': 'Professional garden planting services including flower beds, shrubs, and landscaping design.',
            'Patio': 'Patio cleaning, maintenance, and installation services to enhance your outdoor space.',
            'Garden Clearance': 'Complete garden clearance and waste removal services for overgrown and cluttered gardens.',
            'Hedge Trimming': 'Expert hedge trimming and topiary services to keep your hedges neat and healthy.',
            'Lawn Care': 'Professional lawn care including mowing, treatment, and maintenance for lush green grass.',
            'Maintenance': 'Regular garden maintenance and upkeep services to keep your garden looking its best.',
            'Tree Services': 'Professional tree care including pruning, removal, and maintenance for safety and health.',
            'General': 'Comprehensive gardening services and general outdoor maintenance solutions.'
        }
        return descriptions.get(service_name, f'Professional {service_name.lower()} services in London.')

def test_google_drive_integration():
    """Test the Google Drive integration"""
    
    drive_api = RealGoogleDriveAPI()
    
    print("🔑 TESTING GOOGLE DRIVE API ACCESS")
    print("="*60)
    print("Service account:", drive_api.credentials_json['client_email'])
    print()
    
    # Test authentication
    if drive_api.authenticate():
        print("✅ Authentication successful!")
        
        # Test getting all albums
        albums = drive_api.get_all_service_albums()
        
        if albums:
            print(f"\n✅ SUCCESS! Retrieved {len(albums)} service albums")
            
            # Show sample photos
            print(f"\n📸 SAMPLE PHOTOS:")
            for service_name, album in albums.items():
                if album['photos']:
                    photo = album['photos'][0]
                    print(f"   {service_name}: {photo['name']}")
                    print(f"      Direct URL: {photo['direct_url']}")
                    print()
                    break
        else:
            print("❌ No albums retrieved")
    else:
        print("❌ Authentication failed")
        print("\n📝 TROUBLESHOOTING:")
        print("1. Make sure you've shared all 9 Google Drive folders with:")
        print("   pnm-photo-access@neon-fiber-468814-d9.iam.gserviceaccount.com")
        print("2. Check that the folders contain image files")
        print("3. Verify the service account has 'Viewer' permission")

if __name__ == "__main__":
    test_google_drive_integration()