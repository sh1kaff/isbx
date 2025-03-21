const testBits = async (test, bits) => {
    let response = await fetch("/test", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({test, bits})
    })

    return await response.json();
};


const genBits = async (lang) => {
    let response = await fetch(`/gen/${lang}`);

    return await response.json();
};;


document.querySelector("#gen-bits-button").addEventListener("click", async () => {
    let lang = document.querySelector("#gen-bits-langs").value;
    let response = await genBits(lang);
    let counter = document.querySelector("#gen-bits-area-counter");

    let error_tag = document.querySelector("#test-error");
    if (response.error) {
        error_tag.textContent = `Error: ${response.error}`;
    }
    else {
        document.querySelector("#gen-bits-area").value = response.bits;
        counter.textContent = response.bits.length;
        error_tag.textContent = "";
    }
});


document.querySelector("#test-bits-button").addEventListener("click", async () => {
    let test = document.querySelector("#test-bits-tests").value;
    let bits = document.querySelector("#gen-bits-area").value;

    let response = await testBits(test, bits);

    let error_tag = document.querySelector("#test-error");
    let result_tag = document.querySelector("#result");
    let status_tag = document.querySelector("#status");

    if (response.error) {
        error_tag.textContent = `Error: ${response.error}`;
        result_tag.textContent = "";
        status_tag.textContent = "";
    }
    else {
        result_tag.textContent = `Result: ${response.result}`;

        if (response.result >= 0.01 && response.result <= 1) {
            status_tag.textContent = "Passed";
            status_tag.classList.value = "passed";
        }
        else {
            status_tag.textContent = "Failed";
            status_tag.classList.value = "failed";
        }

        error_tag.textContent = "";
    }
});


document.querySelector("#gen-bits-area").addEventListener("input", (event) => {
    let counter = document.querySelector("#gen-bits-area-counter");
    let count = event.target.value.length;

    counter.textContent = count;
});