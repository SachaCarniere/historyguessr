package historyguessr

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

class StartGameStress extends Simulation {

	val httpProtocol = http
		.baseUrl("http://89.234.182.58:8000")
		.acceptHeader("*/*")
		.acceptEncodingHeader("gzip, deflate")
		.acceptLanguageHeader("fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3")
		.userAgentHeader("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0")

	val scn = scenario("Stress Test - POST Game")
		.exec(http("POST /game").post("http://89.234.182.58:8000/game"))
				.pause(5)

	setUp(scn.inject(atOnceUsers(1000))).protocols(httpProtocol)
}