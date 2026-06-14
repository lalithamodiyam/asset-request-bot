Asset Request Bot - Test Cases

Test Case 1 - Valid Employee ID

Input:
E101

Expected Result:
Employee validated successfully.

Status:
Pass

---

Test Case 2 - Invalid Employee ID

Input:
E999

Expected Result:
Invalid Employee ID message displayed.

Status:
Pass

---

Test Case 3 - Asset Request Submission

Input:
Asset Type: Laptop
Asset Name: Dell Latitude 5440
Reason: Project Development

Expected Result:
Request submitted successfully.
Ticket ID generated.

Status:
Pass

---

Test Case 4 - Auto Approval

Input:
Employee Grade G5

Expected Result:
Status = Approved

Status:
Pass

---

Test Case 5 - Pending Approval

Input:
Employee Grade below G4

Expected Result:
Status = Pending Approval

Status:
Pass

---

Test Case 6 - Request History

Input:
Open Request History Tab

Expected Result:
Stored requests displayed successfully.

Status:
Pass

---

Test Case 7 - Cancel Request

Input:
/cancel

Expected Result:
Request Cancelled message displayed.

Status:
Pass