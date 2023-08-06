import logging
from navigator_session import get_session
from navigator.views import DataView


class ModulesServices(DataView):
    async def get(self):
        """
        ---
        description: Get all user modules on the client
        tags:
        - ModulesServices
        produces:
        - application/json
        parameters:
        - name: sessionid
          description: session of Django
          in: headers
          required: true
          type: string
        responses:
            "200":
                description: returns valid data
            "204":
                description: No data
            "403":
                description: Forbidden Call
        """
        try:
            try:
                session = await get_session(self.request)
                session = session["session"]
                # print('SESSION: ', session)
            except (KeyError, TypeError):
                session = None
            # print("GROUPS ", session, type(session))
            try:
                employee_group = [x for x in session["groups"]]
            except (KeyError, TypeError):
                employee_group = None
            # print(employee_group)
            try:
                client = self.request.get("client")
            except KeyError:
                client = None

            result = None
            if session and employee_group:
                sql = f"select  module_id, module_name, allow_filtering, filtering_show, module_slug, conditions, \
                module_description as description, module_attributes as attributes, program_id, \
                parent_module_id, group_id, group_name from troc.vw_group_modules \
                where client_slug = {client!r} AND group_name = ANY(ARRAY{employee_group!r}) \
                group by module_id, module_name, allow_filtering, filtering_show,conditions, \
                module_slug,  module_description, module_attributes, program_id, parent_module_id, group_id, group_name "
                print("SQL: ", sql)
                await self.connect(self.request)
                try:
                    result = await self.query(sql)
                except Exception as err:
                    logging.error(f"Error on Module Service: {err!s}")
                    result = None
            if result:
                modules_list = [dict(row) for row in result]
                headers = {"x-status": "OK", "x-message": "Module List OK"}
                return self.json_response(
                    response=modules_list, headers=headers, status=200
                )
            else:
                headers = {
                    "x-status": "Empty",
                    "x-message": "Module information not found",
                }
                return self.no_content(headers=headers)
        except Exception as e:
            print(e)
            return self.critical(self.request, e)
        finally:
            await self.close()
