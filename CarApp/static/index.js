document.addEventListener("DOMContentLoaded", function () {
        const serviceInput = document.getElementById("service-cost");
        const costInput = document.querySelector(".service-cost");

        // Predefined costs for each service
        const serviceCosts = {
            "Routine maintenance service": 150,
            "Break service": 120,
            "Engine diagonistic": 200,
            "Suspension and wheel allignments": 180
        };

        serviceInput.addEventListener("input", function () {
            const selectedService = serviceInput.value;

            if (serviceCosts[selectedService] !== undefined) {
                costInput.value = serviceCosts[selectedService];
            } else {
                costInput.value = "";  
            }
        });
    });

