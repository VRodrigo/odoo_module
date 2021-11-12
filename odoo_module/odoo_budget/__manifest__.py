# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Odoo Budget',
    'summary': "Budget",
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Sales',
    'author': 'Victor Rodrigo',
    'website': '',
    'depends': ['sale'],
    'data': [
        "security/contact_security.xml",
        "security/ir.model.access.csv",
        "reports/budget_report.xml",
        "reports/budget_report_templates.xml",
        "views/menu_budget_view.xml",
        "views/budget_view.xml",
        "data/ir_sequence_data.xml"
    ],
    'application': True,
    'installable': True,
}
