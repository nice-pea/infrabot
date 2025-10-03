package ru.dsaime

import com.github.kotlintelegrambot.bot
import com.github.kotlintelegrambot.entities.ChatId
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

class ChatParams(
    val chatId: Long,
    val topic: Long? = null,
)

fun Application.configureRouting(
    chatParams: ChatParams,
//    ghSecret: String,
    tgtoken: String,
) {
//    val bot by inject<Bot>()
    val bot = bot { tgtoken }

    routing {
        get("/") {
            call.respondText("Hello!")
        }
        get("/ping") {
            call.respondText("pong")
        }
        post("/workflows") {
//            if (call.request.queryParameters["secret"] != ghSecret) {
//                return@post call.respondText("", status = HttpStatusCode.Unauthorized)
//            }

            bot.sendMessage(
                chatId = ChatId.Id(chatParams.chatId),
                messageThreadId = chatParams.topic,
                text = call.receiveText(),
            )
        }
    }
}
