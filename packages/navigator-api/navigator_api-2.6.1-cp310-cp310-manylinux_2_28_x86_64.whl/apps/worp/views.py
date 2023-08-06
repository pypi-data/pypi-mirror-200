""""
App Views.
"""
import json
import logging
import operator
from datetime import datetime
from uuid import UUID

from aiohttp import web
from asyncdb.exceptions import NoDataFound, ProviderError, StatementError
from asyncpg.exceptions import UndefinedColumnError, UniqueViolationError
from datamodel.exceptions import ValidationError

from apps.worp.models import POTracker, tracker_defaults
from apps.worp.settings import DEFAULT_PO_NAME
from navigator.views import BaseHandler, BaseView, ModelView


def is_valid_uid(test, version: int = 4):
    try:
        uuid_obj = UUID(test, version=version)
    except ValueError:
        return False
    except Exception:
        pass
    return str(uuid_obj) == test or uuid_obj.hex == test


class TrackerDefaults(BaseHandler):
    """
    Function utilities for managing PO Tracker Handlers.
    """

    async def get_defaults(self, request: web.Request, **kwargs):
        """get_defaults.

        description: returns the default values for PO Tracker.
        """
        headers = {"X-STATUS": "OK", "X-MESSAGE": "PO Tracker Defaults"}
        try:
            return self.json_response(response=tracker_defaults, headers=headers)
        except Exception as err:
            logging.exception(err)
            return self.error(request=request, exception=err, status=409)

    async def set_defaults(self, request: web.Request, **kwargs):
        """set_defaults.

        description: Change and returns the default values for PO Tracker.
        """
        headers = {"X-STATUS": "OK", "X-MESSAGE": "PO Tracker Defaults"}
        # from apps.worp.models import tracker_defaults as td

        data = await self.data(request=request)
        try:
            for key, val in data.items():
                if hasattr(tracker_defaults, key):
                    setattr(tracker_defaults, key, val)
        except Exception as err:
            logging.exception(err)
            return self.error(request=request, exception=err, status=409)
        return self.json_response(response=tracker_defaults, headers=headers)

    async def get_values(self, request: web.Request, **kwargs):
        """set_defaults.

        description: Get PO Tracker calculated values.
        """
        headers = {"X-STATUS": "OK", "X-MESSAGE": "PO Tracker Values"}
        calculated = [
            "store_id",
            "po_number",
            "total_days",
            "merch_headcount",
            "lead_headcount",
            "team_capt_headcount",
            "total_headcount",
            "total_merchant_hours",
            "total_lead_hours",
            "total_capt_hours",
            "total_hours",
            "merch_billable_amount",
            "sup_billable_amount",
            "capt_billable_amount",
            "total_billable_amount",
            "merch_payable_amount",
            "sup_payable_amount",
            "capt_payable_amount",
            "total_payable_amount",
        ]
        data = await self.data(request=request)
        qs = self.get_arguments(request=request)
        if "start_date" in data.keys():
            data["start_date"] = datetime.strptime(
                data["start_date"], "%Y-%m-%d"
            ).date()
        if "end_date" in data.keys():
            data["end_date"] = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
        if "effective_date" in data.keys():
            data["effective_date"] = datetime.strptime(
                data["effective_date"], "%Y-%m-%d"
            ).date()
        if "effective_end_date" in data.keys():
            data["effective_end_date"] = datetime.strptime(
                data["effective_end_date"], "%Y-%m-%d"
            ).date()
        try:
            tracker = POTracker(**data)
        except Exception as err:
            print(err)
            logging.exception(err)
            headers = {"X-STATUS": "FAIL", "X-MESSAGE": "Error: PO Tracker Calculation"}
            return self.error(
                response=f"WORP Error: {err!s}",
                exception=err,
                headers=headers,
                status=409,
            )
        response = tracker.dict()
        try:
            del response["uid"]
        except KeyError:
            pass
        if "calculated" in qs.keys():
            try:
                tmp = {}
                for e in calculated:
                    tmp[e] = response[e]
                response = tmp
            except KeyError:
                pass
        return self.json_response(response=response, headers=headers)

    async def get_trackers(self, request: web.Request, **kwargs):
        """get_trackers.

        description: Get PO Tracker calculated values.
        """
        qs = """
        select p.po_name, p.description, p.start_date, p.end_date, p.is_current, count(store_id) as num_trackers
        FROM worp.po_trackers p
        INNER JOIN worp.po_tracker USING(po_id)
        GROUP BY p.po_name, p.description, p.start_date, p.end_date, p.is_current
        """
        try:
            async with await request.app["database"].acquire() as db:
                result, error = await db.query(qs)
                if error:
                    raise Exception("No PO Trackers")
                trackers = [dict(row) for row in result]
                headers = {"X-STATUS": "OK", "X-MESSAGE": "PO Tracker List"}
                return self.json_response(response=trackers, headers=headers)
        except Exception as err:
            logging.exception(err)
            return self.critical(exception=err, status=500)

    async def get_current(self, request: web.Request, **kwargs):
        """get_current.

        description: GET Current PO Tracker (based on po_id or po_name).
        """
        fields = """
            "po_id", "uid", "po_version", "po_name", "po_number",
            "store_id", "store_name", "market_id", "district_id", "region_id",
            "start_date", "end_date", "effective_date", "effective_end_date",
            "total_days", "project_days", "work_hours_per_day", "total_weeks",
            "hours_per_week", "adjusted_start_date", "adjusted_end_date",
            "adjusted_hours_per_week",
            "merch_headcount", "lead_headcount", "team_capt_headcount",
            "total_headcount",
            "total_merchant_hours", "total_lead_hours", "total_capt_hours",
            "total_hours",
            "billing_rate_merch", "billing_rate_sup", "billing_rate_capt",
            "merch_billable_amount", "sup_billable_amount",
            "capt_billable_amount", "total_billable_amount",
            "pay_rate_merch", "pay_rate_sup", "pay_rate_capt",
            "merch_payable_amount", "sup_payable_amount",
            "capt_payable_amount", "total_payable_amount", "po_billable_amount", "current_po", "notes"
        """
        qs = f"select {fields!s} FROM worp.vw_po_trackers WHERE is_current = true;"
        try:
            async with await request.app["database"].acquire() as db:
                result, error = await db.query(qs.format(fields=fields))
                if error:
                    raise Exception("No PO Trackers")
                trackers = [dict(row) for row in result]
                headers = {"X-STATUS": "OK", "X-MESSAGE": "PO Tracker Current"}
                return self.json_response(response=trackers, headers=headers)
        except Exception as err:
            logging.exception(err)
            return self.critical(exception=err, status=500)


class Tracker(ModelView):
    model = POTracker

    async def get_connection(self):
        try:
            db = await self.request.app["database"].acquire()
            self.model.Meta.connection = db
        except Exception as err:
            raise Exception(f"{err}") from err

    async def get(self):
        headers = {"X-STATUS": "EMPTY", "X-MESSAGE": "PO Tracker not Found"}
        try:
            await self.get_connection()
        except Exception as err:
            logging.exception(err)
            return self.critical(exception=err, status=500)
        try:
            data = await self.data(request=self.request)
        except (TypeError, AttributeError):
            data = {}
        try:
            qs = self.get_arguments()
            params = self.match_parameters()
        except (TypeError, ValueError):
            logging.exception(err)
            params = {}
            qs = {}
        if "uid" in params:
            ## Search only for a single Row (Store)
            try:
                tracker = await self.model.get(**params)
                if not tracker:
                    return self.no_content(headers=headers)
                if "all_versions" in qs:
                    # get all existing version of a row
                    _filter = {
                        "store_id": tracker.store_id,
                        "is_current": True
                        # "po_name": tracker.po_name
                    }
                    print("FILTER> ", _filter)
                    trackers = await self.model.filter(**_filter)
                    if not trackers:
                        return self.no_content(headers=headers)
                    # convert into list of trackers:
                    trackers = [t.dict() for t in trackers]
                    return self.json_response(response=trackers, headers=headers)
                elif "last_version" in qs:
                    # get all existing version of a row
                    _filter = {
                        "store_id": tracker.store_id,
                        "is_current": True
                        # "po_name": tracker.po_name
                    }
                    print("FILTER> ", _filter)
                    trackers = await self.model.filter(**_filter)
                    if not trackers:
                        return self.no_content(headers=headers)
                    else:
                        track = trackers.pop()
                        return self.json_response(response=track, headers=headers)
                else:
                    # return existing row
                    return self.json_response(response=tracker.dict(), headers=headers)
            except UndefinedColumnError as err:
                logging.exception(err)
                response = {
                    "message": f"Invalid Column: {err!s}"
                }
                return self.error(
                    response=response, exception=err, status=406
                )
            except Exception as err:
                logging.exception(err)
                response = {
                    "message": "Unhandler Error",
                    "error": str(err)
                }
                return self.error(response=response, exception=err, status=406)
            finally:
                await self.model.Meta.connection.close()
        else:
            not_current = False
            if "not_current" in qs:
                not_current = True if qs["not_current"] == "true" else False
            if not_current is True:
                # return the not current
                filter = {}
            else:
                filter = {"is_current": True}
            if data:
                filter = {**filter, **data}

            try:
                trackers = await self.model.filter(**filter)
                if not trackers:
                    return self.no_content(headers=headers)
                # convert into list of trackers:
                trackers = [t.dict() for t in trackers]
                return self.json_response(response=trackers, headers=headers)
            except UndefinedColumnError as err:
                logging.exception(err)
                response = {
                    "message": f"Invalid Column: {err!s}"
                }
                return self.error(
                    response=response, exception=err, status=406
                )
            except Exception as err:
                logging.exception(err)
                return self.critical(exception=err, status=500)
            finally:
                await self.model.Meta.connection.close()

    async def patch(self):
        """
        patch.

        Update fields on existing row.
        """
        try:
            await self.get_connection()
        except Exception as err:
            print(err)
            logging.exception(err)
            return self.critical(exception=err, status=500)
        headers = {"X-STATUS": "PO TRACKER OK", "X-MESSAGE": "PO Tracker Updated"}
        to_remove = "start_date"  # we cannot change the start date.-
        try:
            data = await self.json_data()
            filter = self.match_parameters()
        except Exception as err:
            print(err)
        if "uid" in filter:
            # Update single PO Tracker.
            try:
                uid = filter["uid"]
                if is_valid_uid(uid):
                    filter = {"uid": str(UUID(uid, version=4))}
                else:
                    response = {
                        "message": f"WORP: Invalid UUID Format: {filter!s}"
                    }
                    return self.error(
                        response=response, status=406
                    )
                tracker = await self.model.get(**filter)
                if not tracker:
                    headers = {"X-STATUS": "EMPTY", "X-MESSAGE": "PO Tracker not Found"}
                    return self.no_content(headers=headers)
                if tracker.po_version > 1:
                    # remove the conflict columns (start_date, etc)
                    for e in to_remove:
                        try:
                            del data[e]
                        except KeyError:
                            pass
                await tracker.update_values(data)
                # change values, then, recalculate.
                tracker.recalculate()
                await tracker.save()
                headers = {
                    "X-STATUS": "PO TRACKER OK",
                    "X-MESSAGE": "PO Tracker Updated",
                }
                return self.json_response(response=tracker.dict(), headers=headers)
            except NoDataFound:
                response = {
                    "error": f"PO no was found for {filter}"
                }
                return self.error(
                    response=response, status=406
                )
            except UndefinedColumnError as err:
                logging.exception(err)

                return self.error(
                    response=f"Invalid Column: {err!s}", exception=err, status=406
                )
            except Exception as err:
                logging.exception(err)
                return self.critical(exception=err, status=500)
            finally:
                await self.model.Meta.connection.close()
        else:
            # massive update of trackers.
            updated = []
            for elem in data:
                for e in to_remove:
                    try:
                        del elem[e]
                    except KeyError:
                        pass
                # get uid
                try:
                    id = elem["uid"]
                    tracker = await self.model.get(uid=id)
                    if not tracker:
                        headers = {
                            "X-STATUS": "EMPTY",
                            "X-MESSAGE": "PO Tracker not Found",
                        }
                        response = {
                            "error": f"Tracker: Missing UID {id}"
                        }
                        return self.error(
                            response=response, status=406
                        )
                    # updating values
                    await tracker.update_values(elem)
                    # change values, then, recalculate.
                    tracker.recalculate()
                    await tracker.save()
                    updated.append(tracker.dict())
                except NoDataFound:
                    response = {
                        "error": f"PO no was found for {elem}"
                    }
                    return self.error(
                        response=response, status=406
                    )
                except UniqueViolationError as err:
                    return self.error(f"Duplicated Error: {err!s}", status=402)
                except StatementError as err:
                    return self.error(f"Contraint Error: {err!s}", status=402)
                except KeyError:
                    return self.error(
                        response="PO Tracker Record missing Key Column UID", status=406
                    )
            else:
                await self.model.Meta.connection.close()
            # here
            headers = {
                "X-STATUS": "PO TRACKER OK",
                "X-MESSAGE": "PO Trackers List Updated",
            }
            return self.json_response(response=updated, headers=headers)

    async def put(self):
        """
        put.

        Creates a new PO Tracker.
        """
        try:
            await self.get_connection()
        except Exception as err:
            logging.exception(err)
            return self.critical(exception=err, status=500)
        data = await self.json_data()
        _filter = self.match_parameters()
        if "uid" in _filter:
            # Get an existing store and create a new Tracker based on that store.
            uid = _filter["uid"]
            try:
                if is_valid_uid(uid):
                    _filter = {"uid": str(UUID(uid, version=4))}
                    tracker = await self.model.get(**_filter)
                else:
                    # get info about a current store
                    _filter = {"store_id": uid, "is_current": True}
                    trackers = await self.model.filter(**_filter)
                    trackers.sort(key=operator.attrgetter("po_version"))
                    tracker = trackers.pop()
            except Exception as err:
                return self.error(
                    response={
                        "reason": "WORP: Invalid UUID Format",
                        "details": f"WORP UUID Error: Invalid UUID format: {err!s}",
                    },
                    exception=err,
                    status=406,
                )
            finally:
                await self.model.Meta.connection.close()
            try:
                # saving the old-one with new parameters:
                tracker.set_effective_date(data)
                await tracker.save()
                print("SAVING TRACKER:::: ", tracker)
            except Exception as err:
                error = str(err)
                logging.error(error)
                if "unq_no_overlapping_effective_dates" in error:
                    return self.error(
                        response={
                            "reason": "Error: Conflict with existing Tracker, Effective Date overlaps a previous Tracker, HINT: please select another effective date that does not overlap any existing Tracker.",
                            "details": f"WORP Duplicate Error: {error}",
                        },
                        status=406,
                    )
                else:
                    return self.error(
                        response={
                            "reason": f"Error: Conflict with existing Tracker, {err}",
                            "details": f"WORP Duplicate Error: {error}",
                        },
                        status=406,
                    )
            finally:
                await self.model.Meta.connection.close()
            try:
                # check which is the greatest version for this store:
                ft = {"store_id": tracker.store_id}
                ver = await self.model.filter(**ft)
                ver.sort(key=operator.attrgetter("po_version"))
                greatest = ver.pop()
                version = greatest.po_version
            except NoDataFound:
                tracker = None
            except Exception as err:
                greatest = tracker
                version = tracker.po_version
            if not tracker:
                # TODO: know the po_name of the current Tracker.
                # we can create an brand-new store-tracker.
                tracker = POTracker(**data)
            else:
                tracker.po_version = version + 1
                print("VERSION ", tracker.po_version)
                tracker.effective_end_date = None
            new_data = tracker.dict()
            try:
                del new_data["uid"]
            except KeyError:
                pass
            # at now: create them.
            try:
                if data:
                    data = {**new_data, **data}
                    try:
                        del data["uid"]
                        # print(data)
                    except KeyError:
                        pass
                new_tracker = self.model(**data)
                tracker = await new_tracker.insert()
                headers = {
                    "X-STATUS": "PO TRACKER OK",
                    "X-MESSAGE": "PO Tracker INSERTED",
                }
                return self.json_response(response=tracker, headers=headers)
            except ValidationError as ex:
                return self.error(
                    exception={
                        "reason": "WORP Validation error: There are errors in data",
                        "details": f"Validation Error: There are errors in your data: {ex!s}",
                        "payload": ex.payload,
                    },
                    status=400,
                )
            except UniqueViolationError as err:
                return self.error(
                    response={
                        "reason": "WORP Duplicate error: already exists a PO Tracker with the same Start/Effective Date.",
                        "details": f"Duplicate Error: Already Exists an PO Tracker with the same Start/Effective Date: {err!s}",
                    },
                    status=402,
                )
            except StatementError as err:
                if "unq_worp_po_tracker_id" in str(err):
                    response = {
                        "reason": "Error: already exists a PO Tracker with the same version for this store, HINT: please select another version for duplicate.",
                        "details": f"WORP Duplicate Error: {err}",
                    }
                else:
                    response = {
                        "reason": "WORP Error: Error on Duplication, please see *Details* for more information.",
                        "details": f"WORP Duplicate Error: {err}",
                    }
                return self.error(response=response, status=402)
            except Exception as err:
                error = str(err)
                if "unq_worp_po_tracker_id" in error:
                    response = {
                        "reason": "Error: already exists a PO Tracker with the same version for this store, HINT: please select another version for duplicate.",
                        "details": f"WORP Duplicate Error: {error}",
                    }
                elif "unq_no_overlapping_effective_dates" in error:
                    response = {
                        "reason": f"Error: Conflict existing Tracker, Effective Date overlaps a previous Tracker, HINT: please select an Effective Date greater than *{greatest.effective_date}* that does not overlap any existing Tracker.",
                        "details": f"WORP Duplicate Error: {error}",
                    }
                else:
                    response = {
                        "reason": "WORP Error: Error on Duplication, please see *Details* for more information.",
                        "details": f"WORP Duplicate Error: {error}",
                    }
                logging.error(err)
                return self.error(response=response, exception=err, status=406)
            finally:
                await self.model.Meta.connection.close()
        elif "store_id" in data:
            # create a single record for an store:
            try:
                _filter = {"store_id": data["store_id"], "is_current": True}
                trackers = await self.model.filter(**_filter)
                tracker = trackers.pop()
            except Exception:
                tracker = None
            if tracker:
                # we need to create a tracker based on the current one:
                try:
                    # saving the old-one with new parameters:
                    tracker.set_effective_date(data)
                    await tracker.save()
                    # update the current tracker
                    try:
                        # check which is the greatest version for this store:
                        ft = {"store_id": tracker.store_id}
                        ver = await self.model.filter(**ft)
                        greatest = ver.pop()
                        version = greatest.po_version
                    except Exception as err:
                        print(err)
                        version = tracker.po_version
                    tracker.po_version = version + 1
                    print("VERSION ", tracker.po_version)
                    tracker.effective_end_date = None
                except ValidationError as err:
                    print(err)
                    logging.error(err)
                    return self.error(
                        response={
                            "reason": "Can't save the current Tracker, There are errors in Data.",
                            "details": err.payload,
                        },
                        status=406,
                    )
                except NoDataFound:
                    tracker = None
                except Exception as err:
                    logging.error(err)
                    return self.error(
                        response={
                            "reason": "Can't save the current Tracker, Effective/End Date combination will conflict with previous Trackers. Hint: Please check the Effective Date of Previous Trackers.",
                            "details": f"WORP PO Tracker Error: {err!s}",
                        },
                        status=406,
                    )
                finally:
                    await self.model.Meta.connection.close()
            else:
                # TODO: know the po_name of the current Tracker.
                # we can create an brand-new store-tracker.
                try:
                    tracker = POTracker(**data)
                except ValidationError as ex:
                    response = {
                        "reason": "WORP Error: Data Validation Error, please see *Details* for more information.",
                        "details": ex.payload,
                    }
                    return self.error(response=response, status=406)
                except Exception as err:
                    response = {
                        "reason": "WORP Error: Error on insert, please see *Details* for more information.",
                        "details": f"WORP INSERT Error: {err!s}",
                    }
                    logging.error(err)
                    return self.error(response=response, exception=err, status=406)
            new_data = tracker.dict()
            try:
                del new_data["uid"]
            except KeyError:
                pass
            # at now: create them.
            try:
                if data:
                    data = {**new_data, **data}
                    try:
                        del data["uid"]
                    except KeyError:
                        pass
                new_tracker = self.model(**data)
                tracker = await new_tracker.insert()
                headers = {
                    "X-STATUS": "PO TRACKER OK",
                    "X-MESSAGE": "PO Tracker INSERTED",
                }
                return self.json_response(response=tracker, headers=headers)
            except ValidationError as err:
                response = {
                    "reason": "WORP Error: Data Validation Error, please see *Details* for more information.",
                    "details": ex.payload,
                }
                return self.error(response=response, status=406)
            except (ProviderError, StatementError) as err:
                error = str(err)
                if "unq_worp_po_tracker_id" in error:
                    response = {
                        "reason": "Error: already exists a PO Tracker with the same version for this store, HINT: please select another store for insert.",
                        "details": f"WORP INSERT Error: {err}",
                    }
                elif "unq_no_overlapping_effective_dates" in error:
                    response = {
                        "reason": "Error: There are another PO Tracker with the same Start Date, End Date or Effective Date Combination.",
                        "details": f"WORP INSERT Error: {err}",
                    }
                else:
                    response = {
                        "reason": "WORP Error: Error on Insert, please see *Details* for more information.",
                        "details": f"WORP INSERT Error: {err}",
                    }
                return self.error(response=response, exception=err, status=400)
            except Exception as err:
                print("ERROR ", err)
                error = str(err)
                if "unq_worp_po_tracker_id" in error:
                    response = {
                        "reason": "Error: already exists a PO Tracker with the same version for this store, HINT: please select another version for duplicate.",
                        "details": f"WORP INSERT Error: {error}",
                    }
                elif "unq_no_overlapping_effective_dates" in error:
                    response = {
                        "reason": "Error: Conflict existing Tracker, Effective Date overlaps a previous Tracker, HINT: please select an Effective Date that does not overlap any existing Tracker.",
                        "details": f"WORP INSERT Error: {error}",
                    }
                else:
                    print(err, type(err))
                    response = {
                        "reason": "WORP Error: Error on insert, please see *Details* for more information.",
                        "details": f"WORP INSERT Error: {error}",
                    }
                logging.error(err)
                return self.error(response=response, exception=err, status=406)
            finally:
                await self.model.Meta.connection.close()
        else:
            if not data:
                return self.error(
                    "We can't create a PO Tracker without arguments.", status=401
                )
            try:
                id = data["id"]
                del data["id"]
            except KeyError:
                id = 1
            try:
                name = data["po_number"]
                del data["po_number"]
            except KeyError:
                name = DEFAULT_PO_NAME
            try:
                start = data["start_date"]
                del data["start_date"]
            except KeyError:
                return self.error(response="Error: PO Tracker need an Start Date", status=401)
            try:
                end = data["end_date"]
                del data["end_date"]
            except KeyError:
                return self.error(response="Error: PO Tracker need an End Date", status=401)
            try:
                effective = data["effective_date"]
                del data["effective_date"]
            except KeyError:
                effective = "null"
            attributes = {}
            defaults = {
                "hours_per_day": tracker_defaults.hours_per_day,
                "team_capt_headcount": tracker_defaults.team_capt_headcount,
                "billing_rate_merch": tracker_defaults.billing_rate_merch,
                "billing_rate_sup": tracker_defaults.billing_rate_sup,
                "billing_rate_capt": tracker_defaults.billing_rate_capt,
                "pay_rate_merch": tracker_defaults.pay_rate_merch,
                "pay_rate_sup": tracker_defaults.pay_rate_sup,
                "pay_rate_capt": tracker_defaults.pay_rate_capt,
                "special_travel_budget": tracker_defaults.special_travel_budget,
                "special_other_budget": tracker_defaults.special_other_budget,
                "addl_po_reqs": tracker_defaults.addl_po_reqs,
                "walmart_sup_billable_rate": tracker_defaults.walmart_sup_billable_rate,
            }
            if data:
                attributes = {**defaults, **data}
            attributes = json.dumps(attributes)
            sql = f"SELECT * FROM worp.po_tracker_create({name!r}, {id}, {start!r}, {end!r}, {effective!r}, '{attributes}'::jsonb);"
            logging.debug(f"WORP CREATION: {sql}")
            try:
                async with await self.request.app["database"].acquire() as db:
                    row, error = await db.queryrow(sql)
                    if error:
                        raise Exception("No PO Tracker was created")
                    result = dict(row)
                    headers = {"x-status": "OK", "x-message": "PO Tracker Creation OK"}
                    return self.json_response(
                        response=result, headers=headers, status=200
                    )
            except StatementError as err:
                error = str(err)
                headers = {
                    "x-status": "Error",
                    "x-message": "Faild Creation: PO Tracker",
                }
                if "unq_no_overlapping_effective_dates" in error:
                    response = {
                        "response": {
                            "reason": "Current Tracker has conflicting Effective Date with another Tracker",
                            "details": f"Current Tracker has conflict with existing Tracker: {error!s}",
                        },
                        "headers": headers,
                        "status": 406,
                    }
                if "unq_no_overlapping_range_dates" in error:
                    response = {
                        "response": {
                            "reason": "Current Tracker has conflict with other existing Tracker",
                            "details": f"Current Tracker has conflict with existing Tracker: {error!s}",
                        },
                        "headers": headers,
                        "status": 406,
                    }
                elif "range lower" in error:
                    response = {
                        "response": {
                            "reason": "WORP Tracker Error: END DATE need to be greater than START DATE",
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "status": 406,
                    }
                elif "overflow" in error:
                    response = {
                        "response": {
                            "reason": f"TRACKER Overflow: Some values in Pay/Billing Rates are greater than expected values: {error!s}",
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "status": 409,
                    }
                elif "po_tracker_check" in error:
                    response = {
                        "response": {
                            "reason": "TRACKER Error: EFFECTIVE DATE need to be greater than START DATE",
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "status": 409,
                    }
                else:
                    response = {
                        "response": {
                            "reason": error,
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "status": 403,
                    }
                return self.error(**response)
            except Exception as err:
                headers = {"x-status": "Empty", "x-message": "Missing PO Tracker"}
                return self.error(exception=err, headers=headers, status=404)
            finally:
                await self.model.Meta.connection.close()

    async def delete(self):
        """
        delete.

        remove the fields on existing row.
        TODO: Check after delete if a previous version exists and enabled.
        """
        try:
            await self.get_connection()
        except Exception as err:
            print(err)
            logging.exception(err)
            return self.critical(exception=err, status=500)
        try:
            # data = await self.post_data()
            filter = self.match_parameters()
        except Exception as err:
            print(err)
        if "uid" in filter:
            try:
                tracker = await self.model.get(**filter)
                # get if a previous tracker exists:
                # check if exists a previous version for this store:
                ft = {
                    "store_id": tracker.store_id,
                    "po_version": tracker.po_version - 1,
                }
                ver = None
                try:
                    ver = await self.model.get(**ft)
                except Exception:
                    pass
                if tracker:
                    state = await tracker.delete()
                    if ver:
                        # set the end_date, effective_end_date to the values of the deleted tracker:
                        try:
                            ver.effective_end_date = tracker.effective_end_date
                            ver.end_date = tracker.end_date
                            ver.recalculate()
                            await ver.save()
                        except Exception as err:
                            logging.exception(
                                f"Error saving Previous Version of Tracker: {err}"
                            )
                    headers = {"x-status": "OK", "x-message": "PO Tracker DELETED OK"}
                    result = {"message": state, "filter": filter}
                    return self.json_response(
                        response=result, headers=headers, status=201
                    )
            except NoDataFound:
                result = {"message": "DELETE 0", "filter": filter}
                headers = {
                    "x-status": "NOT FOUND",
                    "x-message": "PO Tracker DELETED NOT FOUND",
                }
                return self.json_response(response=result, headers=headers, status=404)
            except Exception as err:
                logging.exception(err)
            finally:
                await self.model.Meta.connection.close()

    async def post(self):
        try:
            await self.get_connection()
        except Exception as err:
            print(err)
            logging.exception(err)
            return self.critical(exception=err, status=500)
        rem = ["inserted_at", "updated_at", "modified_by", "created_by"]
        try:
            data = await self.json_data()
            filter = self.match_parameters()
        except Exception as err:
            print(err)
        if "uid" in filter:
            """Update only a single Store."""
            try:
                uid = filter["uid"]
                if is_valid_uid(uid):
                    filter = {"uid": str(UUID(uid, version=4))}
                else:
                    raise Exception(f"WORP: Wrong format on Tracker UUID: {uid}")
                tracker = await self.model.get(**filter)
                old_effective = tracker.effective_date
                for k in rem:
                    try:
                        del data[k]
                    except KeyError:
                        pass
                if "effective_date" in data.keys():
                    # I will change the effective date
                    try:
                        eff = datetime.strptime(
                            data["effective_date"], "%Y-%m-%d"
                        ).date()
                    except Exception as err:
                        raise Exception(
                            f"WORP: Wrong format in Effective Date: {err!s}"
                        ) from err
                    if eff != old_effective:
                        logging.debug("Creating a new Tracker")
                        # I need to create a new one
                        tracker.set_effective_date(data)
                        await tracker.save()
                        # ---
                        tracker.po_version += 1
                        tracker.effective_end_date = None
                        await tracker.update_values(data)
                        tracker.recalculate()
                        new_data = tracker.dict()
                        try:
                            del new_data["uid"]
                        except KeyError:
                            pass
                        new_tracker = self.model(**new_data)
                        result = await new_tracker.insert()
                        if result:
                            tracker = await self.model.get(**result)
                    else:
                        await tracker.update_values(data)
                        # change values, then, recalculate.
                        tracker.recalculate()
                        # saving the existing
                        await tracker.save()
                else:
                    await tracker.update_values(data)
                    # change values, then, recalculate.
                    tracker.recalculate()
                    # saving the existing
                    await tracker.save()
                headers = {
                    "X-STATUS": "PO TRACKER OK",
                    "X-MESSAGE": "PO Trackers List Updated",
                }
                return self.json_response(response=tracker.dict(), headers=headers)
            except UniqueViolationError as err:
                return self.error(f"Duplicated Error: {err!s}", status=402)
            except StatementError as err:
                return self.error(f"Contraint Error: {err!s}", status=402)
            except Exception as err:
                error = str(err)
                logging.error(err)
                headers = {
                    "x-status": "Error",
                    "x-message": "WORP PO Tracker: Updated Failed.",
                }
                if "unq_no_overlapping_effective_dates" in error:
                    response = {
                        "response": {
                            "reason": f"Current Tracker has conflicting Effective Date with another Tracker",
                            "details": f"Current Tracker has conflict with existing Tracker: {error!s}",
                        },
                        "headers": headers,
                        "status": 406,
                    }
                elif "unq_no_overlapping_range_dates" in error:
                    response = {
                        "response": {
                            "reason": f"Current Tracker has conflict with other existing Tracker",
                            "details": f"Current Tracker has conflict with existing Tracker: {error!s}",
                        },
                        "headers": headers,
                        "status": 406,
                    }
                elif "range lower" in error:
                    response = {
                        "response": {
                            "reason": "WORP Tracker Error: END DATE need to be greater than START DATE",
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "status": 406,
                    }
                elif "overflow" in error:
                    response = {
                        "response": {
                            "reason": f"TRACKER Overflow: Some values in Pay/Billing Rates are greater than expected values: {error!s}",
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "status": 409,
                    }
                elif "po_tracker_check" in error:
                    response = {
                        "response": {
                            "reason": "TRACKER Error: EFFECTIVE DATE need to be greater than START DATE",
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "status": 409,
                    }
                else:
                    response = {
                        "response": {
                            "reason": error,
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "status": 403,
                    }
                return self.error(**response)
            finally:
                await self.model.Meta.connection.close()

    class Meta:
        tablename: str = "po_tracker"
        schema: str = "worp"


class PO_Tracker(BaseView):
    """
    Walmart Overnight PO Tracker.

    Managing the PO Tracker instance, create, reset, delete or update the PO Tracker.
    """

    pass
