package ru.dsaime

import com.github.kotlintelegrambot.Bot
import com.github.kotlintelegrambot.bot
import io.ktor.server.application.*
import org.koin.dsl.module
import org.koin.ktor.plugin.Koin
import org.koin.logger.slf4jLogger

fun Application.configureKoin(tgtoken: String) {
    install(Koin) {
        slf4jLogger()
        modules(
            module {
                single<Bot> { bot { tgtoken } }
            },
        )
    }
}
