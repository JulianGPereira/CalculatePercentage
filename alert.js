function calcAlertsPercentages() {
    var uploadedFile = document.getElementById("data-file").files[0];
    if(uploadedFile){
        var formData = new FormData();
        formData.append('csvFile', uploadedFile);

        fetch("http://localhost:5000/calculateAlerts", {
            method: "POST",
            body: formData,
        })
        .then((response) => {
            const resp = response.json();
            if(response.status == 1001){
                alert('Invalid file. Please select a valid csv file.');
                return false;
            }
            return resp;
        })
        .then((data) => {
            updateTable(data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    } else {
        alert('Please select a csv file');
    }
}

function updateTable(data) {
    const tableBody = document.getElementById("alertTableBody");

    // Iterate over the data and create table rows
    for (let i = 0; i < data.length; i++) {

        const row = document.createElement("tr");

        const empIdCell = document.createElement("td");
        empIdCell.textContent = data[i].empId;
        row.appendChild(empIdCell);

        const totalAlertsCell = document.createElement("td");
        totalAlertsCell.textContent = data[i].noOfAlerts;
        row.appendChild(totalAlertsCell);

        const alertsToTotalCell = document.createElement("td");
        alertsToTotalCell.textContent =
        data[i].alertsToTotal.toFixed(2) + "%";
        row.appendChild(alertsToTotalCell);

        const distressAlertsCell = document.createElement("td");
        distressAlertsCell.textContent = data[i].noOfDistressAlerts;
        row.appendChild(distressAlertsCell);

        const distressAlertsPercentageCell = document.createElement("td");
        distressAlertsPercentageCell.textContent =
        data[i].distressAlertsToSubtotal.toFixed(2) + "%";
        row.appendChild(distressAlertsPercentageCell);

        const fallAlertsCell = document.createElement("td");
        fallAlertsCell.textContent = data[i].noOfFallAlerts;
        row.appendChild(fallAlertsCell);

        const fallAlertsPercentageCell = document.createElement("td");
        fallAlertsPercentageCell.textContent =
        data[i].fallAlertsToSubtotal.toFixed(2) + "%";
        row.appendChild(fallAlertsPercentageCell);

        tableBody.appendChild(row);
 
    }
}