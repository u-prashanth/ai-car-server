import express from 'express'
import socket from 'socket.io'
import cors from 'cors'


const PORT = 4500
const app = express()
// app.use(cors())

const chatServer = app.listen(PORT, () => {
    console.log(`Server running on PORT: ${PORT}`)
})

const io = socket(chatServer)


io.on('connection', (socket) => {

    console.log(`${socket.id} connected`)

    socket.on('disconnect', data => {
        console.log('Client Disconnected: ', socket.id)
    })

    socket.on('connect', (data) => {
        console.log(data, 'has joined')
    })

    socket.join('cam', (err => {
        if(err) console.log(`Unable to Join Camera Feed room`)

        socket.to('cam').broadcast.emit('joined', {
            message: `${socket.id} joined the room`
        })
    }))

    socket.on('cameraFeed', (data) => {
        socket.in('cam').broadcast.emit('cameraFeed', data)
    })

})