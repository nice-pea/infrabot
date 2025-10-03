@file:Suppress("ktlint:standard:no-wildcard-imports")

package ru.dsaime

import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.core.main
import com.github.ajalt.clikt.parameters.options.default
import com.github.ajalt.clikt.parameters.options.help
import com.github.ajalt.clikt.parameters.options.option
import com.github.ajalt.clikt.parameters.options.required
import com.github.ajalt.clikt.parameters.types.int
import io.ktor.server.application.*
import io.ktor.server.cio.*
import io.ktor.server.engine.*

fun main() = Infrabot().main(arrayOf())

fun Application.module() {
    configureSerialization()
    configureDatabases()
    configureRouting()
}

class Infrabot : CliktCommand() {
    val port: Int by option().int().default(8080).help("Порт сервера")
    val telegramToken: String by option().required().help("Токен бота")

    override fun run() {
        embeddedServer(CIO, port = 8080, host = "0.0.0.0", module = Application::module)
            .start(wait = true)
    }
}
