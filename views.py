import logging.config, yaml
from flask.blueprints import Blueprint
from flask import render_template
from sqlalchemy import ForeignKey

from database import db
import util

logging.config.dictConfig(yaml.load(open('logging.conf')))
logger = logging.getLogger('console')
branch = Blueprint('branch', __name__, template_folder='templates')


class Branches(db.Model):
    """ A model for branches table"""
    __tablename__ = 'branches'

    ifsc = db.Column(db.String(), primary_key=True)
    bank_id = db.Column(db.Integer, ForeignKey('banks.id', ondelete='CASCADE'), nullable=False,)
    branch = db.Column(db.String())
    address = db.Column(db.String())
    city = db.Column(db.String())
    district = db.Column(db.String())
    state = db.Column(db.String())

    def __init__(self, ifsc, bank_id, branch, address, city, district, state):
        self.ifsc = ifsc
        self.bank_id = bank_id
        self.branch = branch
        self.address = address
        self.city = city
        self.district = district
        self.state = state


class Banks(db.Model):
    """ A model for banks table"""
    __tablename__ = 'banks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)


@branch.route("/")
def hello():
    """ Default URL to check if service is up"""
    return "Hello there, service is up!"


@branch.route("/branch/ifsc/<ifsccode>")
def get_branch_details(ifsccode):
    """
    Method to fetch branch details based on IFSC Code, accepts ifsccode through URL path.
    Args:
        ifsccode: IFSC Code for which bank's branch details is needed.
    Returns:
        data: A list of single dict with these values- Bank, IFSC Code, Branch, Address, City,
        District, State
    """
    try:
        branch_details = (db.session.query(Branches, Banks).
                          filter(Branches.bank_id == Banks.id).
                          filter(Branches.ifsc == ifsccode).
                          all())
        results = util.prepare_results(branch_details)
        if results:
            return render_template("branch_details.html", data=results)
        return '<p>No results matched your query!</p>'
    except Exception as fault:
        logger.error(fault, exc_info=True)
        logger.error("Something went wrong while fetching branch details. Error: %s", str(fault))
        return "Uh-OH! Something went wrong, we are looking into it."


@branch.route("/branch/bank/<bank>/city/<city>")
def list_all_branches(bank, city):
    """
    Method to fetch all branches of a bank based on bank name and city, accepts args
    through URL path.
    Args:
        bank: Name of the bank.
        city: City where bank branches to be searched.
    Returns:
        data: A list of dict with these values- Bank, IFSC Code, Branch, Address, City,
        District, State
    """
    try:
        branches = (db.session.query(Branches, Banks).
                    filter(Branches.bank_id == Banks.id).
                    filter(Branches.city == city).
                    filter(Banks.name == bank).
                    all())
        results = util.prepare_results(branches)
        if results:
            return render_template("branch_details.html", data=results)
        return '<p>No results matched your query!</p>'
    except Exception as fault:
        logger.error(fault, exc_info=True)
        logger.error("Something went wrong while listing branches. Error: %s", str(fault))
        return "Uh-OH! Something went wrong, we are looking into it."
