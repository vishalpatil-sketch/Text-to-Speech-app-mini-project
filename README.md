<!DOCTYPE html>
<html>
<head>
  <title>Content to Speech</title>
</head>
<body>

<h2>Content to Speech App</h2>

<textarea id="content" rows="10" cols="50"
placeholder="Type or paste text here"></textarea>

<br><br>

<button onclick="readText()">Read Aloud</button>

<script>
function readText() {
  const text = document.getElementById("content").value;
  const speech = new SpeechSynthesisUtterance(text);
  speechSynthesis.speak(speech);
}
</script>

</body>
</html>
