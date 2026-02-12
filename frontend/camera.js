const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const btn = document.getElementById("capture");

navigator.mediaDevices.getUserMedia({ video: true })
.then(stream => {
    video.srcObject = stream;
});

btn.onclick = async () => {

    const ctx = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    ctx.drawImage(video, 0, 0);

    canvas.toBlob(async (blob) => {

        const formData = new FormData();
        formData.append("image", blob, "photo.jpg");

        const res = await fetch(" https://ernesto-bluish-nonserially.ngrok-free.dev/ocr-translate", {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        console.log(data);
        alert("OCR: " + data.ocr_text + "\nTranslated: " + data.translated_text);

    }, "image/jpeg");
};
