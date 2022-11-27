# Copyright (c) 2022, Golive-SOlutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LibraryTransaction(Document):
	def before_submit(self):
		library_member = frappe.get_doc("Library Member", self.library_member)
		if self.transaction_type_section == "Issue":
			self.validate_issue()
			self.self.validate_max_number_of_issued_articles(library_member)
			# set the article status to be Issued
			article = frappe.get_doc("Library Article", self.library_article)
			article.status = "Issued"
			article.save()
			library_member.issued_articles += 1
			library_member.save()

		elif self.transaction_type_section == "Return":
			self.validate_return()
			# set the article status to be Available
			article = frappe.get_doc("Library Article", self.library_article)
			article.status = "Available"
			article.save()
			library_member.issued_articles -= 1
			library_member.save()

	def validate_issue(self):
		self.validate_membership()
		
		article = frappe.get_doc("Library Article", self.library_article)
		# article cannot be issued if it is already issued
		if article.status == "Issued":
			frappe.throw("Article is already issued by another member")

	def validate_return(self):
		article = frappe.get_doc("Library Article", self.library_article)
		# article cannot be returned if it is not issued first
		if article.status == "Available":
			frappe.throw("Article cannot be returned without being issued first")

	def validate_membership(self):
		# check if a valid membership exist for this library member
		valid_membership = frappe.db.exists(
			"Library Membership",
			{
				"library_member": self.library_member,
				"docstatus": 1,
				"from_date": ("<", self.date),
				"to_date": (">", self.date),
			},
		)
		if not valid_membership:
			frappe.throw("The member does not have a valid membership")

	def validate_max_number_of_issued_articles(self,library_member):
		library_settings = frappe.get_single("Library Settings")
		if library_member.issued_articles + 1 > library_settings.maximum_number_of_issued_articles :
			frappe.throw("The member has been reached maximum number of issued articles")


