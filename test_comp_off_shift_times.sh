#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

BASE_URL="http://localhost:8000"
TODAY=$(date +%Y-%m-%d)
SATURDAY=$(date -d "$(date +%w | sed 's/^0$/7/') days" -d "$TODAY" +%Y-%m-%d 2>/dev/null || date -v+6d -f "%Y-%m-%d" "$TODAY" +%Y-%m-%d 2>/dev/null)

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  COMP-OFF WITH SHIFT TIMES TEST${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Testing scenario:"
echo "  • Create comp-off request for Saturday"
echo "  • Approve comp-off request (manager)"
echo "  • Verify schedule shows shift times"
echo ""

# Get auth tokens from setup
echo -e "${YELLOW}Step 1: Getting authentication tokens...${NC}"
ADMIN_LOGIN=$(curl -s -X POST "$BASE_URL/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=Admin@12345")

ADMIN_TOKEN=$(echo $ADMIN_LOGIN | jq -r '.access_token')

if [ "$ADMIN_TOKEN" = "null" ] || [ -z "$ADMIN_TOKEN" ]; then
  echo -e "${RED}✗ Failed to get admin token${NC}"
  exit 1
fi

echo -e "${GREEN}✓ Got admin token${NC}"

# Get departments
echo -e "${YELLOW}Step 2: Fetching departments...${NC}"
DEPTS=$(curl -s -X GET "$BASE_URL/departments" \
  -H "Authorization: Bearer $ADMIN_TOKEN")

DEPT_ID=$(echo $DEPTS | jq -r '.[0].id')
echo -e "${GREEN}✓ Department ID: $DEPT_ID${NC}"

# Get employees
echo -e "${YELLOW}Step 3: Fetching employees...${NC}"
EMPLOYEES=$(curl -s -X GET "$BASE_URL/employees?department_id=$DEPT_ID" \
  -H "Authorization: Bearer $ADMIN_TOKEN")

EMP_ID=$(echo $EMPLOYEES | jq -r '.[0].id')
EMP_NAME=$(echo $EMPLOYEES | jq -r '.[0].first_name')
EMP_ROLE=$(echo $EMPLOYEES | jq -r '.[0].role_id')

echo -e "${GREEN}✓ Employee: $EMP_NAME (ID: $EMP_ID, Role: $EMP_ROLE)${NC}"

# Get roles to find shifts
echo -e "${YELLOW}Step 4: Fetching role shifts...${NC}"
ROLES=$(curl -s -X GET "$BASE_URL/roles?department_id=$DEPT_ID" \
  -H "Authorization: Bearer $ADMIN_TOKEN")

SHIFT=$(echo $ROLES | jq -r ".[0].shifts[0]" 2>/dev/null)
SHIFT_START=$(echo $SHIFT | jq -r '.start_time')
SHIFT_END=$(echo $SHIFT | jq -r '.end_time')

echo -e "${GREEN}✓ Shift Times: $SHIFT_START - $SHIFT_END${NC}"

# Get manager token
echo -e "${YELLOW}Step 5: Getting manager token...${NC}"
MANAGER_LOGIN=$(curl -s -X POST "$BASE_URL/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=manager001&password=Manager@123")

MANAGER_TOKEN=$(echo $MANAGER_LOGIN | jq -r '.access_token')
echo -e "${GREEN}✓ Got manager token${NC}"

# Create comp-off request
echo -e "${YELLOW}Step 6: Creating comp-off request for Saturday ($SATURDAY)...${NC}"
COMP_OFF_REQ=$(curl -s -X POST "$BASE_URL/comp-off-requests" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"employee_id\": $EMP_ID,
    \"comp_off_date\": \"$SATURDAY\",
    \"reason\": \"Test comp-off with shift times\"
  }")

COMP_OFF_ID=$(echo $COMP_OFF_REQ | jq -r '.id')

if [ "$COMP_OFF_ID" = "null" ] || [ -z "$COMP_OFF_ID" ]; then
  echo -e "${RED}✗ Failed to create comp-off request${NC}"
  echo "Response: $COMP_OFF_REQ"
  exit 1
fi

echo -e "${GREEN}✓ Comp-off request created (ID: $COMP_OFF_ID)${NC}"

# Approve comp-off
echo -e "${YELLOW}Step 7: Manager approving comp-off...${NC}"
APPROVAL=$(curl -s -X POST "$BASE_URL/manager/approve-comp-off/$COMP_OFF_ID" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"review_notes\": \"Approved for testing\"}")

echo -e "${GREEN}✓ Comp-off approved${NC}"

# Fetch schedule to verify shift times are set
echo -e "${YELLOW}Step 8: Fetching schedule for Saturday...${NC}"
SCHEDULES=$(curl -s -X GET "$BASE_URL/schedules?start_date=$SATURDAY&end_date=$SATURDAY" \
  -H "Authorization: Bearer $ADMIN_TOKEN")

COMP_OFF_SCHED=$(echo $SCHEDULES | jq -r ".[] | select(.employee_id == $EMP_ID and .date == \"$SATURDAY\")")
SCHED_STATUS=$(echo $COMP_OFF_SCHED | jq -r '.status')
SCHED_START=$(echo $COMP_OFF_SCHED | jq -r '.start_time')
SCHED_END=$(echo $COMP_OFF_SCHED | jq -r '.end_time')

echo -e "${GREEN}Schedule Details:${NC}"
echo "  Status: $SCHED_STATUS"
echo "  Start Time: $SCHED_START"
echo "  End Time: $SCHED_END"

# Verify shift times are populated
if [ "$SCHED_START" = "null" ] || [ -z "$SCHED_START" ]; then
  echo -e "${RED}✗ FAILED: Shift times not populated in comp-off schedule${NC}"
  echo "Full schedule: $COMP_OFF_SCHED"
  exit 1
else
  echo -e "${GREEN}✓ Shift times successfully populated in comp-off schedule${NC}"
fi

# Verify status is comp_off_taken
if [ "$SCHED_STATUS" != "comp_off_taken" ]; then
  echo -e "${RED}✗ FAILED: Schedule status should be 'comp_off_taken', got '$SCHED_STATUS'${NC}"
  exit 1
else
  echo -e "${GREEN}✓ Schedule status is 'comp_off_taken'${NC}"
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ ALL TESTS PASSED - Comp-off with shift times working correctly!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Summary:"
echo "  • Comp-off request approved for: $EMP_NAME"
echo "  • Date: $SATURDAY"
echo "  • Shift times displayed: $SCHED_START - $SCHED_END"
echo "  • Status: $SCHED_STATUS (employee off but shift times shown)"
