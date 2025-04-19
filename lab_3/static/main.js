let ALLOWEDKEYS = [
    "rsa_public_key",
    "rsa_private_key",
    "cast5_encrypted_key"
];


async function generateKeys(cast5_keylen = 128) {
    let response = await fetch(
        "/generate",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json;charset=utf-8"
            },
            body: JSON.stringify({cast5_keylen}) 
        }
    );

    if (!response.ok) {
        let error = (await response.json())["message"];
        throw `Error: ${error}`
    }

    return await response.json();
}


function updateError(text = "") {
    let errorTag = document.querySelector("#error");
    errorTag.textContent = text;
    if (!text) {
        errorTag.hidden = true;
    } else {
        errorTag.hidden = false;
    }
}


function getFileName(response, default_name) {
    const contentDisposition = response.headers.get('Content-Disposition');
    if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/i);
        if (filenameMatch && filenameMatch[1]) {
            return filenameMatch[1];
        }
    }

    return default_name
}


function downloadBlob(blob, filename) {
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();

    setTimeout(() => {
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }, 100);
}


function changeDownloadHidden() {
    div = document.querySelector("#download_keys");
    div.hidden = false;
}


async function downloadKey(key) {   
    console.log(key);

    if (!ALLOWEDKEYS.includes(key)) {
        throw "Key not allowed";
    }

    let response = await fetch(
        `/keys/${key}`,
        {
            method: "GET"
        }
    )

    if (!response.ok) {
        let error = (await response.json())["message"];
        throw `Error: ${error}`
    } 

    const blob = await response.blob();
    downloadBlob(
        blob,
        getFileName(response, key + ".pem")
    )
}


async function encrypt(decrypt = false) {
    let action = (decrypt) ? "decrypt" : "encrypt";
    
    let input = document.querySelector(`#${action} input`)
    let data = new FormData()

    let file = input.files[0]
    if (!file) {
        throw "No file"
    }

    data.append('file', file)

    let response = await fetch(
        `/${action}`, 
        {
            method: "POST",
            body: data
        }
    )

    if (!response.ok) {
        let error = (await response.json())["message"];
        throw `Error: ${error}`
    } 

    const blob = await response.blob();
    downloadBlob(
        blob,
        getFileName(response, `file.${action.slice(0, 3)}`)
    )
}


async function uploadKeys() {
    let [input1, input2] = document.querySelectorAll("#upload_keys input")

    let file1 = input1.files[0]
    let file2 = input2.files[0]

    if (!file1 || !file2) {
        throw "No files"
    }

    let data = new FormData()
    data.append('rsa_private_key', file1)
    data.append('cast5_encrypted_key', file2)

    let response = await fetch(
        "/keys", 
        {
            method: "POST",
            body: data
        }
    )

    if (!response.ok) {
        let error = (await response.json())["message"];
        throw `Error: ${error}`
    }

    return await response.json()
}


document.querySelector("#encrypt button").addEventListener("click", async function(event) {
    try {
        await encrypt();
    } catch (error) {
        updateError(error);
        return;
    }

    updateError();
    alert("Encrypted")
});


document.querySelector("#decrypt button").addEventListener("click", async function(event) {
    try {
        await encrypt(true);
    } catch (error) {
        updateError(error);
        return;
    }

    updateError();
    alert("Decrypted")
});


document.querySelector("#upload_keys button").addEventListener("click", async function(event) {
    try {
        await uploadKeys();
    } catch (error) {
        updateError(error);
        return;
    }

    changeDownloadHidden();
    updateError();
    alert("Uploaded");
});


document.querySelector("#generate button").addEventListener("click", async function(event) {
    try {
        let CAST5Keylen = Number(document.querySelector("#generate input").value)
        await generateKeys(CAST5Keylen);
    } catch (error) {
        updateError(error);
        return;
    }

    changeDownloadHidden();
    updateError();
    alert("Generated");
});


document.querySelectorAll("#download_keys button").forEach(function (button) {
    button.addEventListener("click", async function(event) {
        try {
            await downloadKey(button.id)
        } catch (error) {
            updateError(error);
            return;
        }
        updateError()
        alert("Downloaded");
    });
});
