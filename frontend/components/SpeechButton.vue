<template>
  <div>
    <button @click="toggleListening">
      {{ listening ? '停止' : '音声認識を開始' }}
    </button>
    <div v-if="listening">
      <p>音声を入力中...</p>
      <!-- 入力状況に応じたUIの変更をここに追加 -->
    </div>
    <div v-if="audioUrl">
      <p>音声データを再生中...</p>
      <audio :src="audioUrl" controls />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const listening = ref(false)
const audioUrl = ref('')
let mediaRecorder = null
let audioChunks = []
let stream = null

const toggleListening = async () => {
  if (listening.value) {
    stopRecognition()
  } else {
    startRecognition()
  }
}

const startRecognition = () => {
  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((mediaStream) => {
      stream = mediaStream // MediaStreamを保存
      listening.value = true
      mediaRecorder = new MediaRecorder(stream)
      audioChunks = []

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data)
      }

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
        // for debug
        // audioUrl.value = URL.createObjectURL(audioBlob)

        // TODO: GoogleAPI用の実装
        sendAudio(audioBlob)
      }

      mediaRecorder.start()
    })
    .catch((error) => {
      console.error('マイクのアクセスに失敗しました：', error)
    })
}

const stopRecognition = () => {
  if (mediaRecorder) {
    mediaRecorder.stop()
    listening.value = false

    // MediaStreamのトラックを停止
    if (stream) {
      stream.getTracks().forEach((track) => track.stop())
      stream = null
    }
  }
}

// TODO: GoogleAPI用の実装
const sendAudio = async (audioBlob) => {
  const formData = new FormData()
  formData.append('audio', audioBlob, 'recording.wav')

  try {
    // エンドポイントURLを /api/process_audio に変更
    const response = await fetch('http://localhost:5050/api/process_audio_test', {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json()
      console.error('バックエンドエラー：', errorData.error)
      return
    }

    const text = await response.json()
    console.log(text)
    // const blob = await response.blob()
    // audioUrl.value = URL.createObjectURL(blob)
    // playAudio()
  } catch (error) {
    console.error('音声送信エラー：', error)
  }
}

// const playAudio = () => {
//   const audio = new Audio(audioUrl.value)
//   audio.play()
// }
</script>

<style scoped>
button {
  padding: 10px 20px;
  font-size: 16px;
}
p {
  margin-top: 10px;
  font-size: 14px;
}
</style>
