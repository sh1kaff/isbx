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
};


document.querySelector("#gen-bits-button").addEventListener("click", async () => {
    let lang = document.querySelector("#gen-bits-langs").value;
    let response = await genBits(lang);

    let error_tag = document.querySelector("#test-error");
    if (response.error) {
        error_tag.innerHTML = `<p>Error: ${response.error}</p>`;
    }
    else {
        document.querySelector("#gen-bits-area").value = response.bits;   
        error_tag.innerHTML = "";
    }
});


document.querySelector("#test-bits-button").addEventListener("click", async () => {
    let test = document.querySelector("#test-bits-tests").value;
    let bits = document.querySelector("#gen-bits-area").value;

    let response = await testBits(test, bits);

    let error_tag = document.querySelector("#test-error");
    let result_tag = document.querySelector("#result");

    if (response.error) {
        error_tag.innerHTML = `<p>Error: ${response.error}</p>`;
        result_tag.innerHTML = "";
    }
    else {
        result_tag.innerHTML = `<p>Result: ${response.result}</p>`;
        error_tag.innerHTML = "";
    }
});