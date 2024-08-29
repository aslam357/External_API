import xmlrpc.client
server_url = 'http://localhost:5656/'
database_name = 'aslamdb'
user_name = 'admin'
user_password = 'admin'

#logging in
common_proxy = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(server_url))
odoo_version = common_proxy.version()
print("Odoo version:", odoo_version)

user_id = common_proxy.authenticate(database_name, user_name, user_password, {})

#calling methods
object_proxy = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))

has_access = object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})
print("Access Rights:", has_access)

#list records
company_ids = object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'search', [[['is_company', '=', True]]])
print("Company IDs:", company_ids)

#pagination
limited_company_ids = object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'search', [[['is_company', '=', True]]], {'offset': 10, 'limit': 5})
print("Subset Company IDs:", limited_company_ids)

#count records
company_count = object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'search_count', [[['is_company', '=', True]]])
print("Company Count:", company_count)

#read records
single_company_id = object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'search', [[['is_company', '=', True]]], {'limit': 1})
[company_record] = object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'read', [single_company_id])
print("Single Company Record:", company_record, "Length:", len(company_record))

selected_company_fields = object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'read', [single_company_id], {'fields': ['name', 'country_id', 'comment']})
print("Selected Fields:", selected_company_fields)

#list record fields
partner_model_fields = object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'fields_get', [], {'attributes': ['string', 'help', 'type']})
print("Model Fields:", partner_model_fields)

#search & read
search_read_companies = object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'search_read', [[['is_company', '=', True]]], {'fields': ['name', 'country_id', 'comment'], 'limit': 5})
print("Search Read Results:", search_read_companies)

#create records
new_partner_id = object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'create', [{'name': "New Partner"}])
print("New Partner ID:", new_partner_id)

#update records
object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'write', [[new_partner_id], {'name': "Updated Partner Name"}])
updated_partner = object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'read', [[new_partner_id], ['display_name']])
print("Updated Partner:", updated_partner)

#delete records
object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'unlink', [[new_partner_id]])
deleted_partner_check = object_proxy.execute_kw(database_name, user_id, user_password, 'res.partner', 'search', [[['id', '=', new_partner_id]]])
print("Deleted Partner Check:", deleted_partner_check)
