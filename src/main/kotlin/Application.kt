package ru.dsaime

import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.core.main
import com.github.ajalt.clikt.parameters.options.default
import com.github.ajalt.clikt.parameters.options.help
import com.github.ajalt.clikt.parameters.options.option
import com.github.ajalt.clikt.parameters.options.required
import com.github.ajalt.clikt.parameters.types.int
import com.github.ajalt.clikt.parameters.types.long
import io.ktor.server.cio.*
import io.ktor.server.engine.*

fun main(args: Array<String>) = Infrabot().main(args)

class Infrabot : CliktCommand() {
    val port: Int by option().int().default(8080).help("Порт сервера")
    val tgtoken: String by option().required().help("Токен бота")
    val chatId: Long by option().long().required().help("ID чата")
    val topic: Long by option().long().required().help("ID треда")
    val ghSecret: String by option().required().help("Секретный ключ GitHub")

    override fun run() {
        embeddedServer(CIO, port = port, host = "0.0.0.0", module = {
//            configureKoin(tgtoken)
            configureRouting(ChatParams(chatId, topic), tgtoken)
        })
            .start(wait = true)
    }
}
