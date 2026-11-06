# Copyright 2026 The ADK Demo Agent Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""In-memory order store for the demo. Every lookup is scoped to one customer."""

from __future__ import annotations

_ORDERS: dict[str, dict[str, str]] = {
    "A-1001": {"customer_id": "cust-ada", "status": "shipped", "total": "42.00"},
    "A-1002": {"customer_id": "cust-ada", "status": "processing", "total": "18.50"},
    "B-2001": {"customer_id": "cust-bob", "status": "delivered", "total": "99.99"},
}

_REFUND_REQUESTS: list[dict[str, str]] = []


def _owned_order(customer_id: str, order_id: str) -> dict[str, str] | None:
  order = _ORDERS.get(order_id)
  if order is None or order["customer_id"] != customer_id:
    return None
  return order


def get_status(customer_id: str, order_id: str) -> dict[str, str]:
  """Returns the status of `order_id` if it belongs to `customer_id`."""
  order = _owned_order(customer_id, order_id)
  if order is None:
    return {"error": "Order not found."}
  return {"order_id": order_id, "status": order["status"]}


def list_for_customer(customer_id: str) -> list[dict[str, str]]:
  """Returns the orders that belong to `customer_id`."""
  return [
      {"order_id": order_id, "status": order["status"]}
      for order_id, order in _ORDERS.items()
      if order["customer_id"] == customer_id
  ]


def open_refund_request(customer_id: str, order_id: str, reason: str) -> dict[str, str]:
  """Records a refund request for review by the support team."""
  if _owned_order(customer_id, order_id) is None:
    return {"error": "Order not found."}
  _REFUND_REQUESTS.append(
      {"customer_id": customer_id, "order_id": order_id, "reason": reason[:500]}
  )
  return {"order_id": order_id, "refund_request": "submitted for review"}
