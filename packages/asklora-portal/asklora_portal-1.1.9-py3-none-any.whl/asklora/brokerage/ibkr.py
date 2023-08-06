from base64 import b64decode
from copy import deepcopy
from datetime import date
from typing import Optional

from asklora.brokerage.client import BaseRestClient
from asklora.brokerage.enums import (
    AccountStatusType,
    DAMAllowedCurrenciesEnum,
    DAMEnumerationsTypeEnum,
)
from asklora.brokerage.models import (
    BrokerResponse,
    DAMApplicationPayload,
    InstructionSet,
    CASearchRequest,
)
from asklora.brokerage.vars import DAMSettings
from asklora.dam import DAM
from asklora.logger import logger
from asklora.pgp import PGPHelper


class DAMECAClient(BaseRestClient):
    def __init__(self):
        # check environment variables
        dam_settings = DAMSettings()

        # assign attributes
        self.base_payload = dict(CSID=dam_settings.DAM_CSID)

        super().__init__(base_url=dam_settings.DAM_ECA_URL)

    # ===================== Schema and Healthcheck =====================

    def check_api(self) -> dict:
        return self.post("healthcheck", self.base_payload)

    def get_enumerations(
        self,
        enum_type: DAMEnumerationsTypeEnum,
        currency: Optional[str] = None,
        form_number: Optional[str] = None,
    ) -> str:
        if enum_type == DAMEnumerationsTypeEnum.EDD_AVT and form_number is None:
            raise ValueError("Need form number data for this enum type")

        if enum_type == DAMEnumerationsTypeEnum.FIN_INFO_RANGES and currency is None:
            raise ValueError("Need currency data for this enum type")

        payload = self.base_payload
        payload["type"] = enum_type.value

        if currency:
            if currency not in DAMAllowedCurrenciesEnum:
                raise ValueError("Invalid currency code")

            payload["currency"] = currency

        if form_number:
            payload["formNumber"] = form_number

        response = self.post("getEnumerations", self.base_payload, raw_response=True)
        decoded_response = b64decode(response).decode("utf-8")

        return decoded_response

    # ===================== Create Accounts and Updating Account Information =====================

    def create_account(
        self,
        applicant_data: DAMApplicationPayload,
        pgp_helper: PGPHelper,
    ) -> BrokerResponse:
        logger.info("Sending account creation payload to ECA endpoint")

        payload = self.base_payload
        payload["payload"] = DAM.generate_application_payload(
            applicant_data,
            pgp_helper=pgp_helper,
        )

        # send the response
        response: dict = self.post("create", data=payload)

        # add more context to the response
        response_data = BrokerResponse(
            url=f"{self.base_url}/create",
            raw_payload=applicant_data.generate_application_xml(),
            payload=payload,
            raw_response=deepcopy(response),
            response=response,
        )

        try:
            response_data.response = DAM.handle_registration_response(
                response,
                pgp_helper=pgp_helper,
            )
            logger.debug(f"Response:\n{response_data.response}")
        except Exception:
            pass

        return response_data

    # ===================== View Account Information and Registration Tasks =====================

    def get_pending_tasks(
        self,
        account_ids: Optional[list[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> dict:
        payload = self.base_payload

        if account_ids:
            payload["accountIds"] = account_ids

        if start_date and end_date:
            payload["startDate"] = start_date
            payload["endDate"] = end_date

        return self.post("getPendingTasks", payload)

    def get_registration_tasks(
        self,
        account_ids: Optional[list[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        get_docs: Optional[bool] = None,
    ) -> dict:
        logger.info("Checking registration tasks")

        payload = self.base_payload

        if account_ids:
            payload["accountIds"] = account_ids

        if get_docs is not None:
            payload["getDocs"] = "T" if get_docs else "F"

        if get_docs is None and (start_date and end_date):
            payload["startDate"] = start_date
            payload["endDate"] = end_date

        response = self.post("getRegistrationTasks", payload)
        logger.info(f"Response:\n{response}")

        return response

    def get_account_details(self, account_ids: list[str]) -> dict:
        payload = self.base_payload
        payload["accountIds"] = account_ids

        return self.post("getAccountDetails", payload)

    def get_account_status(
        self,
        account_ids: list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        status: AccountStatusType | str | None = None,
    ) -> dict:
        payload = self.base_payload

        if account_ids:
            payload["accountIDs"] = account_ids
        if start_date:
            payload["startDate"] = start_date
        if end_date:
            payload["endDate"] = end_date
        if status:
            if isinstance(status, AccountStatusType):
                status = status.value
            payload["status"] = status

        return self.post("getAccountStatus", payload)


class DAMCAClient(BaseRestClient):
    """Client class for IBKR's Corporate Actions endpoint (https://www.ibkrguides.com/dameca/CorpAction/submit.htm)"""

    def __init__(self):
        # check environment variables
        dam_settings = DAMSettings()

        # assign attributes
        self.base_payload = dict(CSID=dam_settings.DAM_CSID)

        super().__init__(base_url=dam_settings.DAM_CA_URL)

    # --------------------------------- Corporate actions -------------------------------- #
    def ca_search_request(
        self,
        action_type: str,
        account_id: int,
        username: int,
        sub_accounts: str,
        from_date: date,
        to_date: date,
        pgp_helper: PGPHelper,
    ) -> BrokerResponse:
        request = CASearchRequest(
            corp_action_type=action_type,
            account_id=account_id,
            sub_accounts_choice=sub_accounts,
            from_date=from_date,
            to_date=to_date,
        )
        request_xml = request.to_xml(
            pretty_print=True,
            encoding="UTF-8",
            skip_empty=True,
            xml_declaration=True,
        ).decode()

        encoded_payload = DAM.encode_file_payload(
            request_xml,
            file_name="search.txt",
            pgp_helper=pgp_helper,
        )

        payload = self.base_payload
        payload["base64Payload"] = encoded_payload
        payload["username"] = username

        response = self.post("", payload)

        # add more context to the response
        response_data = BrokerResponse(
            url=self.base_url,
            raw_payload=request_xml,
            payload=payload,
            raw_response=deepcopy(response),
            response=response,
        )

        if "details" in response:
            response["details"] = DAM.decode_xml_response(
                response.get("details"),
                pgp_helper=pgp_helper,
            )
            response_data.response = response

        return response_data


class DAMFBClient(BaseRestClient):
    def __init__(self):
        # check environment variables
        dam_settings = DAMSettings()

        # assign attributes
        self.base_payload = dict(CSID=dam_settings.DAM_CSID)

        super().__init__(base_url=dam_settings.DAM_FB_URL)

    def create_instruction(
        self,
        instruction: InstructionSet | str,
        pgp_helper: PGPHelper,
    ) -> BrokerResponse:
        if isinstance(instruction, InstructionSet):
            instruction = instruction.to_xml(
                pretty_print=True,
                encoding="UTF-8",
                skip_empty=True,
                xml_declaration=True,
            ).decode()

        encoded_instruction = DAM.encode_file_payload(
            instruction,
            file_name="instructions.xml",
            pgp_helper=pgp_helper,
        )

        payload = self.base_payload
        payload["request"] = encoded_instruction

        # send the request
        response = self.post("new-request", payload)

        # add more context to the response
        response_data = BrokerResponse(
            url=f"{self.base_url}/new-request",
            raw_payload=instruction,
            payload=payload,
            raw_response=deepcopy(response),
            response=response,
        )

        if "details" in response:
            response["details"] = DAM.decode_xml_response(
                response.get("details"),
                pgp_helper=pgp_helper,
            )
            response_data.response = response

        return response_data

    def get_status(self, instruction_id: int, pgp_helper: PGPHelper) -> BrokerResponse:
        encoded_instruction_ids = DAM.encode_file_payload(
            str(instruction_id),
            file_name="instruction_ids.txt",
            pgp_helper=pgp_helper,
        )

        payload = self.base_payload
        payload["instruction_set_id"] = encoded_instruction_ids

        response = self.post("get-status", payload)

        # add more context to the response
        response_data = BrokerResponse(
            url=f"{self.base_url}/get-status",
            raw_payload=instruction_id,
            payload=payload,
            raw_response=deepcopy(response),
            response=response,
        )

        if "details" in response:
            response["details"] = DAM.decode_xml_response(
                response.get("details"),
                pgp_helper=pgp_helper,
            )
            response_data.response = response

        return response_data

    def get_updates(self, since: date | str, pgp_helper: PGPHelper) -> BrokerResponse:
        since = since if isinstance(since, str) else since.strftime("%Y-%m-%d")

        encoded_date = DAM.encode_file_payload(
            since,
            file_name="instruction_ids.txt",
            pgp_helper=pgp_helper,
        )

        payload = self.base_payload
        payload["since_yyyy-mm-dd"] = encoded_date

        response = self.post("get_updated_upload_ids", payload)

        # add more context to the response
        response_data = BrokerResponse(
            url=f"{self.base_url}/get_updated_upload_ids",
            raw_payload=since,
            payload=payload,
            raw_response=deepcopy(response),
            response=response,
        )

        if "details" in response:
            response["details"] = DAM.decode_xml_response(
                response.get("details"),
                pgp_helper=pgp_helper,
            )
            response_data.response = response

        return response_data
