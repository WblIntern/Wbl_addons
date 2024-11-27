from odoo import http
from odoo.http import request
from datetime import datetime


class PortalMyProductDetailsPdf(http.Controller):
    @http.route(['/product/details/category/pdf'], methods=["GET"], auth='public', website=True)
    def portal_my_product_details_pdf(self, **kw):
        print("=====button clicked=====")
        # Fetch all products
        # products = request.env['product.template'].sudo().search([])
        products = request.env['product.template'].sudo().search([('website_published', '=', True)])
        print("=====xxx=====", products)

        # Prepare values for the template
        products_data = []
        for product in products:
            print("===",product.image_128)
            # Collect attributes for each product
            attributes = []
            for attribute_line in product.attribute_line_ids:
                for value in attribute_line.value_ids:
                    attributes.append({
                        'attribute': attribute_line.attribute_id.name,
                        'value': value.name,
                    })

            products_data.append({
                'name': product.name,
                'description': product.description_sale or '',
                'image': product.image_128,
                'price': f"{product.list_price:.2f}",
                'currency_symbol': product.currency_id.symbol or '',
                'attributes': attributes,
            })

            print("======products_data", products_data)

        current_date = datetime.today().strftime('%Y-%m-%d')

        values = {
            'products': products_data,
            'current_date': current_date,
        }

        # Render the PDF
        report_service = request.env['ir.actions.report']
        pdf_content, _ = report_service._render_qweb_pdf('wbl_website_pdf_catalog.action_report_all_product_template',
                                                         [], values)

        # Create a response to download the PDF
        response = request.make_response(pdf_content, headers=[
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', 'attachment; filename="all_products_details.pdf"'),
        ])
        return response

# from odoo import http
# from odoo.http import request
# from datetime import datetime
#
#
# ##############   THIS CONTROLLER IS USED TO PRINT THE PRODUCT PDF ON PRODUCT CATEGORY PRINT BUTTON CLICK ############
# class PortalMyProductDetailsPdf(http.Controller):
#     @http.route(['/product/details/category/pdf'], methods=["GET"], auth='public', website=True)
#     def portal_my_product_details_pdf(self, product_id, **kw):
#         # Fetch the product record using the product_id
#         # settings = request.env['res.config.settings'].sudo().get_values()
#         # print("====settings===", settings)
#
#         if product_id:
#             product = request.env['product.template'].sudo().browse(int(product_id))
#             print("Product Fetched:", product)  # Check if the product is fetched
#
#             # Collect attributes and values
#             attributes = []
#             for attribute_line in product.attribute_line_ids:
#                 attribute = attribute_line.attribute_id
#                 print("Attribute Fetched:", attribute.name)  # Check if attributes are fetched
#
#                 for value in attribute_line.value_ids:
#                     print(" - Value Fetched:", value.name)  # Check if values are fetched
#                     attributes.append({
#                         'attribute': attribute.name,
#                         'value': value.name
#                     })
#
#             # Get other product details
#             currency_symbol = product.currency_id.symbol or ''
#             formatted_price = f"{product.list_price:.2f}"
#
#             current_date = datetime.today().strftime('%Y-%m-%d')
#
#             # Pass all values to the template
#             values = {
#                 'product': product,
#                 'name': product.name,
#                 'list_price': formatted_price,
#                 'currency_symbol': currency_symbol,
#                 'image': product.image_1920,
#                 'description': product.description_ecommerce or '',
#                 'attributes': attributes,
#                 'current_date': current_date,
#             }
#             print("Values to Render:", values)  # Print values before rendering
#
#             # Generate the PDF using the 'ir.actions.report' service with the correct report action ID
#             report_service = request.env['ir.actions.report']
#             pdf_content, _ = report_service._render_qweb_pdf('wbl_website_pdf_catalog.action_report_all_product_template',
#                                                              [product.id], values)
#
#             # Create a response that triggers the file download
#             response = request.make_response(pdf_content, headers=[
#                 ('Content-Type', 'application/pdf'),
#                 ('Content-Disposition', f'attachment; filename="{"product"}_details.pdf"'),
#             ])
#
#             return response
