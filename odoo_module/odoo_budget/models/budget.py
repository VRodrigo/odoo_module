from odoo import api, fields, models, _


class Budget(models.Model):
    _name = 'budget'
    _rec_name = 'name'
    _description = 'Budget'

    @api.depends('budget_line_ids.total', 'displacement_ids.price')
    def _compute_total(self):
        for record in self:
            total = 0
            for line in record.budget_line_ids:
                total += line.total
            for line in record.displacement_ids:
                total += line.price
            record.update({'total': total})

    name = fields.Char(string='name', required=True,
                       default=lambda self: _('New'))
    date = fields.Date(string='Date')
    partner_id = fields.Many2one('res.partner', string='Customer')
    budget_line_ids = fields.One2many('budget.line', 'budget_id',
                                      string='Budget Lines', required=True)
    displacement_ids = fields.One2many('displacement.line', 'budget_id',
                                       string='Displacements')
    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 index=True,
                                 default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users', 'Salesperson', required=True,
                              index=True,
                              default=lambda self: self.env.user.id)
    currency_id = fields.Many2one(related='company_id.currency_id',
                                  depends=["company_id"], store=True)
    total = fields.Monetary(string='Total', compute='_compute_total',
                            readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'budget') or _('New')
        result = super(Budget, self).create(vals)
        return result


class BudgetLine(models.Model):
    _name = 'budget.line'
    _description = 'Budget Line'
    _order = 'budget_id'

    @api.depends('quantity', 'price_unit', 'discount')
    def _compute_line_total(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            line.update({"total": price * line.quantity})

    budget_id = fields.Many2one('budget', string='Budget')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string=' Price Unit',
                              digits='Product Unit of Measure', default=0.0)
    discount = fields.Float(string='Discont', digits='Discount', default=0.0)
    currency_id = fields.Many2one(related='budget_id.currency_id',
                                  depends=['budget_id.currency_id'],
                                  store=True, string='Currency',
                                  readonly=True)
    company_id = fields.Many2one(related='budget_id.company_id',
                                 string='Company', store=True,
                                 readonly=True, index=True)
    total = fields.Monetary(string='Total', compute='_compute_line_total',
                            store=True, readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.price_unit = self.product_id.list_price


class DisplacementLines(models.Model):
    _name = 'displacement.line'
    _description = 'Displacement Line'
    _order = 'budget_id'

    budget_id = fields.Many2one('budget', string='Budget')
    address = fields.Char(string='Address')
    date = fields.Date(string='Date')
    price = fields.Float(string=' Price Unit',
                         digits='Product Unit of Measure', default=0.0)
