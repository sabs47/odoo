# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Devintelle Solutions (<http://devintellecs.com/>).
#
##############################################################################
from odoo import api, fields, models


class Partenr(models.Model):
    _inherit = "res.partner"

    survey_id = fields.Many2one(
        'survey.survey', "Survey Form",
        help="Choose an interview form for this job position and you will be able to print/answer this interview from all applicants who apply for this job")
    response_id = fields.Many2one('survey.user_input', "Response", ondelete="set null", oldname="response")
    survey_histroy_id = fields.One2many('survey.user_input', 'partner_id',string ="Resultas Audits")

    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if self.survey_id:
            response = self.env['survey.user_input'].create({'survey_id': self.survey_id.id, 'partner_id': self.id})
            self.response_id = response.id
        # grab the token of the response and start surveying
        return self.survey_id.with_context(survey_token=response.token).action_start_survey()

    def action_print_survey(self):
        """ If response is available then print this response otherwise print survey form (print template of the survey) """
        self.ensure_one()
        if not self.response_id:
            return self.survey_id.action_print_survey()
        else:
            response = self.response_id
            return self.survey_id.with_context(survey_token=response.token).action_print_survey()

    def survey_url(self):
        if self.survey_id:
            if self.survey_id:
                response = self.env['survey.user_input'].create({'survey_id': self.survey_id.id, 'partner_id': self.id})
                self.response_id = response.id
            survey_data = self.survey_id.with_context(survey_token=response.token).action_start_survey()
            print ("survey_data======",survey_data)
            print ("url======",survey_data['url'])
            return survey_data['url']
