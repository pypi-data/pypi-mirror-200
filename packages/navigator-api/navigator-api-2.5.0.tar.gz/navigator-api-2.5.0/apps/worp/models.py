"""
WORP PO Tracker Models.

Orders Tracker for Walmart Overnight Program.
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from asyncdb.drivers.postgres import postgres
from asyncdb.meta import Record
from asyncdb.models import Column, Model

from navigator.conf import asyncpg_url

"""
AsyncDB Models
"""
MODELS = {}


def auto_now_add(*args, **kwargs):
    return str(uuid.uuid4())


@dataclass
class TrackerDefaults:
    hours_per_day: int = field(default=8)
    hours_per_week: float = field(default=40.0)
    team_capt_headcount: int = field(default=1)
    merch_headcount: int = field(default=15)
    lead_headcount: int = field(default=4)
    billing_rate_merch: float = field(default=16.0)
    billing_rate_sup: float = field(default=14.0)
    billing_rate_capt: float = field(default=40.0)
    pay_rate_merch: float = field(default=14.0)
    pay_rate_sup: float = field(default=12.0)
    pay_rate_capt: float = field(default=30.0)
    special_travel_budget: int = field(default=0)
    special_other_budget: int = field(default=0)
    addl_po_reqs: int = field(default=0)
    walmart_sup_billable_rate: int = field(default=0)


tracker_defaults = TrackerDefaults()

store_info = """
select store_number, store_name, market_id, district_id, region_id,
merch_number as merch_headcount,
supervisor_number as lead_headcount, project_days
FROM worp.stores where store_id = '{store_id}' and store_active = true;
"""

po_info = """
select po_id FROM worp.po_trackers WHERE start_date = '{start_date}'
AND end_date = '{end_date}' AND is_current = true
"""


class POTracker(Model):
    uid: str = Column(required=True, primary_key=True, db_default="uuid_generate_v4()")
    """ Fields asked to User."""
    po_id: int = Column(required=True, default=1)
    po_version: int = Column(required=True, default=1)
    po_name: str = Column(required=False)
    po_number: str = Column(required=False)
    po_range: range = Column(required=False)
    effective_range: range = Column(required=False)
    store_id: str = Column(required=True)
    store_name: str = Column(required=False)
    market_id: int = Column(required=False)
    district_id: int = Column(required=False)
    region_id: int = Column(required=False)
    # dates:
    start_date: datetime = Column(required=True)
    end_date: datetime = Column(required=True)
    effective_date: datetime = Column(required=False)
    """ End field asked."""
    effective_end_date: datetime = Column(required=False)
    total_days: int = Column(required=False, default=0)
    project_days: int = Column(required=False, default=8)
    work_hours_per_day: int = Column(default=tracker_defaults.hours_per_day)
    total_weeks: float = Column(required=False, default=8.57)
    hours_per_week: float = Column(required=False, default=40)
    adjusted_start_date: date
    adjusted_end_date: date
    adjusted_hours_per_week: int
    """ Store Info (per-store)."""
    merch_headcount: int = Column(required=False)
    lead_headcount: int = Column(required=False)
    team_capt_headcount: int = Column(default=tracker_defaults.team_capt_headcount)
    total_merchant_hours: float
    total_lead_hours: float
    total_capt_hours: float
    """ End Store Info."""
    total_headcount: int
    total_hours: float
    billing_rate_merch: float = Column(
        required=False, default=tracker_defaults.billing_rate_merch
    )
    billing_rate_sup: float = Column(
        required=False, default=tracker_defaults.billing_rate_sup
    )
    billing_rate_capt: float = Column(
        required=False, default=tracker_defaults.billing_rate_capt
    )
    pay_rate_merch: float = Column(
        required=False, default=tracker_defaults.pay_rate_merch
    )
    pay_rate_sup: float = Column(required=False, default=tracker_defaults.pay_rate_sup)
    pay_rate_capt: float = Column(
        required=False, default=tracker_defaults.pay_rate_capt
    )
    # billing rates
    merch_billable_amount: float
    sup_billable_amount: float
    capt_billable_amount: float
    total_billable_amount: float
    po_billable_amount: float = Column(required=True, default=0)
    # payable rates
    merch_payable_amount: float
    sup_payable_amount: float
    capt_payable_amount: float
    total_payable_amount: float
    """ Optional Fields. """
    special_travel_budget: float
    special_other_budget: float
    addl_po_reqs: float
    walmart_sup_billable_rate: float = Column(default=0.0)
    walmart_merch_billable_rate: float = Column(default=0.0)
    deficit_surplus_hours: float = Column(default=0.0)
    deficit_surplus_dollars: float = Column(default=0.0)
    is_current: bool = Column(required=False, default=True)
    """ End of PO Tracker Fields."""
    inserted_at: datetime = Column(
        required=False, default=datetime.now(), db_default="now()"
    )
    updated_at: datetime = Column(required=False, default=datetime.now())
    modified_by: str = Column(default=None)
    created_by: str = Column(default=None)
    notes: str = Column(default=None)

    def __post_init__(self):
        # ID:
        if not self.po_id:
            self.po_id = 1
        # versioning:
        if not self.po_version:
            self.po_version = 1
        if not self.uid:
            self.uid = str(auto_now_add())
        if not self.start_date:
            self.start_date = datetime.utcnow().date()
        if not self.end_date:
            self.end_date = datetime.now().date()
        if type(self.start_date) == str:
            # convert to date
            self.start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        if type(self.end_date) == str:
            # convert to date
            self.end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()
        if not self.effective_date:
            self.effective_date = self.start_date
        elif type(self.effective_date) == str:
            # convert to date
            self.effective_date = datetime.strptime(
                self.effective_date, "%Y-%m-%d"
            ).date()
        if not self.effective_end_date:
            self.effective_end_date = self.end_date
        elif type(self.effective_end_date) == str:
            # convert to date
            self.effective_end_date = datetime.strptime(
                self.effective_end_date, "%Y-%m-%d"
            ).date()
        # PO NAME
        if not self.po_name:
            dt_format = self.start_date.strftime("%m-%Y")
            self.po_name = f"{self.po_number}-{dt_format}"
        # calculation of total weeks
        self.total_days = self.num_days()
        self.total_weeks = self.num_weeks()
        # Total Headcount
        # self.team_capt_headcount = self.team_capt_headcount if self.team_capt_headcount > 0 else tracker_defaults.team_capt_headcount
        # getting Store Defaults values.
        try:
            self.store_defaults()
        except Exception:
            raise
        # PO dates:
        self.po_dates()
        # calculating headcounts:
        self.total_headcount = (
            self.merch_headcount + self.lead_headcount + self.team_capt_headcount
        )
        self.total_hours = self.get_total_hours()
        self.billing_rates(
            self.billing_rate_merch, self.billing_rate_sup, self.billing_rate_capt
        )
        self.payable_rates()
        self.other_expenses()
        # convert uuid to string:
        self.uid = str(self.uid)

    def get_total_hours(self):
        return self.total_merchant_hours + self.total_lead_hours + self.total_capt_hours

    def num_days(self):
        if not self.effective_end_date:
            self.effective_end_date = self.end_date
        # TODO
        # making calculation about previous version
        return (self.effective_end_date - self.effective_date).days + 1

    def num_weeks(self, week_days: int = 7):
        return (self.total_days) / 7

    def get_store_info(self, store_id):
        db = postgres(dsn=asyncpg_url)
        with db.connect() as conn:
            # first: use the same connection to got the PO ID:
            # GET ID of Current PO
            try:
                id, error = conn.fetchone(
                    po_info.format(start_date=self.start_date, end_date=self.end_date)
                )
                if error:
                    self.po_id = None
                elif not id:
                    self.po_id = None
                else:
                    self.po_id = id["po_id"]
            except Exception as err:
                self.po_id = None
                logging.exception(f"WORP: No Tracker was detected: {err!s}")
            try:
                result, error = conn.fetchone(store_info.format(store_id=store_id))
                if not result:
                    raise Exception(f"WORP Store Not found: {store_id}")
                if error:
                    raise Exception(error)
            except Exception:
                raise
            return Record.from_dict(dict(result))

    def store_defaults(self):
        """
        TODO: calculated based on Store.
        """
        if not self.store_name:
            try:
                store = self.get_store_info(self.store_id)
            except Exception:
                raise
            if self.merch_headcount is None:
                self.merch_headcount = store.merch_headcount
            if self.lead_headcount is None:
                self.lead_headcount = store.lead_headcount
            self.project_days = store.project_days
            # store information:
            self.store_name = store.store_name
            self.market_id = store.market_id
            self.district_id = store.district_id
            self.region_id = store.region_id
        # Store-based calculations
        self.work_hours_per_day = tracker_defaults.hours_per_day
        # self.hours_per_week = (self.project_days * self.work_hours_per_day)
        self.hours_per_week = tracker_defaults.hours_per_week
        self.total_merchant_hours = (
            self.merch_headcount * self.total_weeks
        ) * self.hours_per_week
        self.total_lead_hours = (
            self.lead_headcount * self.total_weeks
        ) * self.hours_per_week
        self.total_capt_hours = (
            self.team_capt_headcount * self.total_weeks
        ) * self.hours_per_week

    def po_dates(self):
        # TODO: get adjusted logic from previous.
        pass
        self.adjusted_start_date = self.start_date
        self.adjusted_end_date = self.end_date
        self.adjusted_hours_per_week = self.hours_per_week

    def billing_rates(
        self,
        billing_rate_merch: float,
        billing_rate_sup: float,
        billing_rate_capt: float,
    ):
        """Getting the basic billing rates."""
        self.merch_billable_amount = float(self.total_merchant_hours) * float(
            billing_rate_merch
        )
        self.sup_billable_amount = float(self.total_lead_hours) * float(
            billing_rate_sup
        )
        self.capt_billable_amount = float(self.total_capt_hours) * float(
            billing_rate_capt
        )
        self.total_billable_amount = (
            self.merch_billable_amount
            + self.sup_billable_amount
            + self.capt_billable_amount
        )

    def payable_rates(self):
        """Getting the basic billing rates."""
        self.merch_payable_amount = float(self.total_merchant_hours) * float(
            self.pay_rate_merch
        )
        self.sup_payable_amount = float(self.total_lead_hours) * float(
            self.pay_rate_sup
        )
        self.capt_payable_amount = float(self.total_capt_hours) * float(
            self.pay_rate_capt
        )
        self.total_payable_amount = (
            self.merch_payable_amount
            + self.sup_payable_amount
            + self.capt_payable_amount
        )

    def other_expenses(self):
        self.special_travel_budget = tracker_defaults.special_travel_budget
        self.special_other_budget = tracker_defaults.special_other_budget
        self.addl_po_reqs = tracker_defaults.addl_po_reqs
        self.walmart_sup_billable_rate: tracker_defaults.walmart_sup_billable_rate
        # TODO: how to calculate those
        self.walmart_merch_billable_rate = 0
        self.deficit_surplus_hours = 0
        self.deficit_surplus_dollars = 0.0

    async def update_values(self, values: dict):
        dates = ("start_date", "end_date", "effective_date", "effective_end_date")
        for key, val in values.items():
            if key in dates:
                value = datetime.strptime(val, "%Y-%m-%d").date()
                if key == "end_date":
                    if self.end_date != value:
                        if "effective_end_date" not in values.keys():
                            self.effective_end_date = value
                setattr(self, key, value)
            else:
                if hasattr(self, key):
                    print(key, val)
                    setattr(self, key, val)

    def recalculate(self):
        if type(self.start_date) == str:
            # convert to date
            self.start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        if type(self.end_date) == str:
            # convert to date
            self.end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()
        if not self.effective_date:
            self.effective_date = self.start_date
        if type(self.effective_date) == str:
            # convert to date
            self.effective_date = datetime.strptime(
                self.effective_date, "%Y-%m-%d"
            ).date()
        if not self.effective_end_date:
            self.effective_end_date = self.end_date
        elif type(self.effective_end_date) == str:
            # convert to date
            self.effective_end_date = datetime.strptime(
                self.effective_end_date, "%Y-%m-%d"
            ).date()
        ###

        self.effective_range = None  # [self.effective_date, self.effective_end_date]
        if not self.po_name:
            dt_format = self.start_date.strftime("%m-%Y")
            self.po_name = f"{self.po_number!s}-{dt_format!s}"
        self.total_days = self.num_days()
        self.total_weeks = self.num_weeks()
        self.team_capt_headcount = (
            self.team_capt_headcount
            if self.team_capt_headcount > 0
            else tracker_defaults.team_capt_headcount
        )
        print(" SET NEW EFFECTIVE ")
        print(self.effective_date, self.effective_range)
        # getting Store Defaults values.
        try:
            self.store_defaults()
        except Exception:
            raise
        # PO dates:
        self.po_dates()
        # calculating headcounts:
        self.total_headcount = (
            self.merch_headcount + self.lead_headcount + self.team_capt_headcount
        )
        self.total_hours = self.get_total_hours()
        self.billing_rates(
            self.billing_rate_merch, self.billing_rate_sup, self.billing_rate_capt
        )
        self.payable_rates()
        self.other_expenses()

    async def save(self):
        self.updated_at = datetime.utcnow()
        self.uid = uuid.UUID(self.uid, version=4)
        await super(POTracker, self).update()

    def set_effective_date(self, data: dict):
        # the effective date will remains the same, but:
        try:
            effective = datetime.strptime(data["effective_date"], "%Y-%m-%d").date()
            self.effective_end_date = effective - timedelta(days=1)
            print("NEW EFFECTIVE DATE ", effective, self.effective_end_date)
        except KeyError:
            pass
        # recalculate all values based on new data:
        # change values, then, recalculate.
        self.recalculate()

    class Meta:
        driver = "pg"
        name = "po_tracker"
        schema = "worp"
        app_label = "worp"
        strict = False
