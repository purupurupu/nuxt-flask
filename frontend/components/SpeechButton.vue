<script setup lang="ts">
import { ref } from 'vue'

interface Response {
  text: string
}

const listening = ref(false)
const audioUrl = ref('')
const responseData = ref<Response | null>(null)
let mediaRecorder: MediaRecorder | null = null
let audioChunks: BlobPart[] | undefined = []
let stream: MediaStream | null = null

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
        audioChunks?.push(event.data)
      }

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
        // for debug
        // audioUrl.value = URL.createObjectURL(audioBlob)

        // GoogleAPI用の実装
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

// GoogleAPI用の実装
// バイナリデータとして音声を送信
const sendAudio = async (audioBlob: Blob) => {
  const formData = new FormData()
  formData.append('audio', audioBlob, 'recording.wav')

  try {
    const response = await fetch('http://localhost:5050/api/process_audio', {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json()
      console.error('バックエンドエラー：', errorData.error)
      return
    }

    // レスポンスが音声データ（Blob）の場合
    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    audioUrl.value = url
    responseData.value = { text: '音声が正常に処理されました。' } // 必要に応じてテキストを追加

    playAudio()
  } catch (error) {
    console.error('音声送信エラー：', error)
  }
}

const playAudio = () => {
  if (audioUrl.value) {
    const audio = new Audio(audioUrl.value)
    audio.play().catch((error) => {
      console.error('音声再生エラー：', error)
    })
  }
}
</script>

<template>
  <div class="flex flex-col items-center w-full">
    <UButton
      :label="listening ? '停止' : '音声認識を開始'"
      :color="listening ? 'red' : 'primary'"
      size="md"
      @click="toggleListening"
    />

    <UAlert v-if="listening" class="mt-4 text-center" color="blue" title="音声を入力中..." />

    <div v-if="responseData" class="mt-4">
      <UAlert color="primary" title="音声データを再生中..." />
      <audio v-if="audioUrl" :src="audioUrl" controls class="mt-2" />
    </div>
    <UAlert
      v-if="responseData?.text"
      class="mt-4"
      color="white"
      title="レスポンス"
      :description="responseData.text"
    />
  </div>
</template>
