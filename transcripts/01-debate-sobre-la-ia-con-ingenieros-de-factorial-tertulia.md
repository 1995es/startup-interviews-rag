# Debate sobre la IA con ingenieros de Factorial | Tertulia de itnig

*301 intervenciones · 10 interlocutores: SPEAKER_00, SPEAKER_01, SPEAKER_02, SPEAKER_03, SPEAKER_04, SPEAKER_05, SPEAKER_06, SPEAKER_07, SPEAKER_08, SPEAKER_09*

> **Canal** Itnig · **Vídeo** [`i-ZOzESUG4U`](https://www.youtube.com/watch?v=i-ZOzESUG4U) · **Publicado** 2026-04-03 · **Duración** 1 h 30 min
>
> Transcripción automática con WhisperX (`large-v2`) + alineación por palabra +
> diarización con `pyannote/speaker-diarization-3.1`. `SPEAKER_XX` son etiquetas
> automáticas, no nombres: la diarización agrupa voces, no las identifica.
> Ni el texto ni el reparto de turnos están revisados a mano.

`00:00:00` **SPEAKER_02** — En el punto en el que estamos ahora es en construir AI a esa serie. Es decir, en facilitar la AI y llevarla cerca de nuestros clientes. ¿No sentís que lleváis la neurona al máximo en estos momentos? O sea, que estamos viendo la capacidad del ser humano ahí al límite, al límite. Tú ves que el cuello de botella es producción. Ahora mismo, para LLM, es seguro. Porque todos sabemos que en el largo plazo hay AGI. La pregunta es, ¿qué va a pasar mañana? Entonces, en este debate de cuál es el perfil que funciona en Factorio, junior, senior, staff, mid, no sé qué, ¿qué ves tú? ¿Qué piensas de ahí? La característica principal para una persona que rinde es... Pedimos a la gente que se ubicara en más o menos believers de la IA. La mayor parte de la gente estaba en no believers, pero ahora, unos meses más tarde,

`00:00:40` **SPEAKER_03** — pues yo creo que ya no quedaría nadie que se ubicaba como no cree en la IA. ¿Tú en qué fase estás?

`00:00:45` **SPEAKER_07** — No escribo código directamente. Ni una línea. Ni una línea. Desde hace meses.

`00:00:49` **SPEAKER_06** — Desde hace meses. El problema nunca había sido generar código. El problema es saber qué código escribir y precisamente detectar esos patrones, o sea, pensar en sistemas. Ese es el problema.

`00:00:59` **SPEAKER_03** — Pero claro, escribir código que es escribir código, ¿no? No lo tecleo, pero el código que se genera yo lo tengo en la cabeza. Me gusta todavía tener el control de cómo la gente está pensando y entonces sé qué código va a generar.

`00:01:09` **SPEAKER_02** — Nunca me había pasado de hacer una demo y yo ser el que más flipa y de golpe Juan le pinta un dashboard exactamente como si leyera el cerebro todo lo que está pidiendo. La gente flipa.

`00:01:18` **SPEAKER_08** — ¡Yo primero! Bienvenidos a la tertulia de Irving.

`00:01:25` **SPEAKER_02** — Esta semana tenemos una tertulia un tanto especial. Estamos en la oficina de Factorial. Por fin, por fin la oficina de Factorial funciona, existe, de ingeniería, de ingeniería y de producto. Y hoy tengo a varios ingenieros de Factorial que pasaban por aquí y os he liado, ¿no? Y vamos a hablar de IA, obviamente, y de en qué etapas estamos ahora mismo en Factorial y vosotros personalmente, ¿vale? Se ha colado un PM. ¿Se ha colado un PM? Porque dado que ha hecho un montón de pull requests últimamente. Relativo, vale, vale. Te he colado yo como neoingeniero, ¿vale? Y aquí habrá un poco la discusión de cuál es el rol del PM y hasta qué punto hay un solapamiento en el ingeniero se vuelve PM y el PM se vuelve ingeniero, ¿vale? Pero antes de esto vamos a repasar un poco las fases del cambio de mindset. que hace seis meses o hace un año, la mayoría de gente... De hecho, hicimos un ejercicio en Factorial donde pedimos que la gente se ubicara en una sala grande en la Costa Brava, que estábamos haciendo un off-site. Pedimos a la gente que se ubicara en más o menos believers de la IA. ¿No? Y la gente, pues, se ubicó, ¿no? Y yo creo que la mayor parte de la gente estaba en no believers, de la IA, ¿no? Sí, fue hace tiempo, hace tiempo. Entonces, los frikis y tal, que estábamos ahí como believers, sin tener ni puta idea de lo que significaba todavía, ¿vale? Pero ahora, unos meses más tarde, pues yo creo que ya, si hiciéramos el mismo ejercicio, no quedaría nada, nadie. Ojalá, ojalá. Pero no quedaría nadie en el que se ubicaba como no cree en la IA. Aunque Edu Seco, lo estoy viendo aquí, es bastante reticente, no la IA, Pero tú eres el que dijiste que lo más relevante no era el 90% automatizable, sino el 10% no automatizable.

`00:03:26` **SPEAKER_03** — Claro, o sea, yo más que eso, lo que perdí es el interés en lo que se puede hacer con la parte de ByteCoding. Me interesa qué es lo que no puedo hacer, en qué se atasca, en qué problema se está atascando.

`00:03:38` **SPEAKER_02** — Pero primero hay que hacer, o sea...

`00:03:40` **SPEAKER_03** — Sí, pero a mí...

`00:03:42` **SPEAKER_02** — Este 90% hay que hacerlo.

`00:03:43` **SPEAKER_03** — Sí, pero a mí personalmente me interesa menos eso, ¿no? Es un problema que no está resuelto, pero alguien va a resolverlo. El tooling madurará. Cada vez la barrera de entrada para usar estas herramientas cada vez es más bajo. Y creo que el problema no estará ahí. Hoy sí que está ahí, pero no estará ahí de aquí a un año o dos años.

`00:04:02` **SPEAKER_02** — O sea, a ti lo que te preocupa es lo que no es computable. Sí.

`00:04:07` **SPEAKER_03** — No, porque al final es computable. Pero son problemas difíciles de entender. Elegir la solución también. No es solo entender el problema. Hay una serie de soluciones que todas son válidas, pero elegir la buena, esto no te lo hace un LLM. Te da una o te da opciones. ¿Pero cuál es la buena? ¿Cuál es la que te convence a ti? ¿Qué criterio sigues para elegir cuál sí y cuál no?

`00:04:31` **SPEAKER_02** — Por cierto, interrumpiros, por favor, no me hagáis hacer de moderador todo el rato.

`00:04:34` **SPEAKER_05** — Por eso yo quiero, ¿por qué no ves que el LM ahora, con todos los OPUS y GPTs que tenemos, y sí? tiene contexto bien puesto, no puede elegir opinión en la mayoría de casos.

`00:04:45` **SPEAKER_03** — ¿Dónde se lía? Al final es lo que a mí me convence o no me convence. Si a mí el output no me convence, pues no estás eligiendo bien. Entonces mueves el problema a cómo le doy el contexto para que haga la solución que a mí me parece la correcta. y eso del tema de ingeniería de contexto, y qué contexto hay, la memoria, en base a que yo tomo decisiones, en base a que para mí la solución esta es correcta y la otra es incorrecta. ¿Cuál es la razón?

`00:05:13` **SPEAKER_05** — Voy a pinchar ahí. Pero esto es basado en el nivel de staff developer, con la barra de excelencia de staff developer. Y si ponemos como, y tenemos, queremos hacer un poco de average de un developer mid o senior,

`00:05:27` **SPEAKER_02** — ¿Has hablado de Staff Developer? Sí. ¿Qué es un Staff Developer? Para la gente que no te escucha igual, que tiene que entender. Buena pregunta. Que no es fácil de responder. ¿Qué es un Staff Developer?

`00:05:38` **SPEAKER_06** — Yo resumiré con más años de experiencia de momento y impacto más horizontal y no solo enfocado en un solo producto, en una cosa, sino impacto en toda la empresa.

`00:05:50` **SPEAKER_02** — O sea, ¿Staff implica años de experiencia?

`00:05:54` **SPEAKER_06** — Bueno, se implica impacto, pero es difícil poder hacer este impacto sin tener años de experiencia. Como a todo, para ser experto en algo necesitas las 10.000 horas, ¿no? O no sé cuántas.

`00:06:10` **SPEAKER_09** — Bueno, yo creo que aquí, en este podcast, tenemos un candidato a no tener que dar toda esa experiencia para ser staff. O sea, siempre hay alguien que rompe un poco ese molde. Pero yo creo que a ti, Edu, lo que te motiva, porque tú eres ingeniero, o sea, lo llevas en la mente, lo que te mola es ese 5% que todavía no es capaz de resolver la IA y que tú te ves con esa capacidad. Es lo que te motiva, ese reto a resolver lo que la IA todavía no es capaz de hacerlo correctamente. No es tanto el…

`00:06:39` **SPEAKER_03** — Sí, lo otro lo veo ya como problemas solucionados. Sé que no están solucionados, pero estarán solucionados.

`00:06:45` **SPEAKER_02** — Pero la pregunta es, ¿qué es el 90 y qué es el 10?

`00:06:50` **SPEAKER_06** — Por ejemplo, cosas que me doy cuenta y que al final es solo porque le falta contexto, le faltan instrucciones, pero la capacidad para hacer las cosas las tiene. Pero, por ejemplo, yo reviso muchos pull requests. Por ejemplo, en One, y me doy cuenta de que hay 10 equipos que están haciendo la misma cosa de maneras muy similares. Esto normalmente pide, igual necesitamos una abstracción, unificar todo para que no todo mundo repita. Ya no es tanto por repetir código, sino para tener una respuesta estructurada. No tenemos ahora mismo... algo a un agent que vaya detectando todos estos patrones y proponga una nueva abstracción. Yo creo que la capacidad la tiene. Si yo le digo, mira todos estos pull requests e intenta encontrar una abstracción, lo hará. Pero se lo tengo que decir yo. ¿Cómo hacemos para que sea reactivo sin intervención humana?

`00:07:48` **SPEAKER_05** — Tú tienes que encontrar el problema. Tú dices esto, ¿no?

`00:07:50` **SPEAKER_06** — Exacto, nosotros creo que aún somos mejores encontrando estos problemas o detectando esas cosas que de momento, bueno, no lo hemos probado simplemente en poner un agent y ve haciendo lo que quieras con todos los pull request, lo podríamos probar.

`00:08:06` **SPEAKER_08** — Y esto antes como era desde hace cinco años, ¿Revisabas tantas PRs que eran muy parecidas entre sí? ¿O es que ahora, como hay tanto músculo y tanta capacidad, de repente tenemos muchísimas más PRs? O sea, mi capacidad de revisar push requests

`00:08:19` **SPEAKER_06** — es la misma ahora que hace un tiempo, simplemente hay otras que se quedan sin revisar, porque hay mucho más código que revisar que antes. Ahora creo que el coño de botella que tenemos es eso, porque aún hablando del nivel en que estamos de AI, Al menos nosotros aún revisamos el código y no confiamos ciegamente en todo lo que se genera. INTERLOCUTOR 1 Voy a

`00:08:41` **SPEAKER_05** — hacerte un poco más de challenge. Aquí, yo revisando pull request, veo que estamos enfocándonos más a nivel de abstracción mucho más alta comparado con antes. Porque todas las cosas básicas que mira todos esos, no sé, scopes o problemas o algunas cosas de síntaxi, Igual. Esto, Copilot u otros, cogen muy bien. Y por eso tú ves ahorros o oportunidades de otro nivel.

`00:09:07` **SPEAKER_06** — Sí, sí, te lo compro. Puedo centrarme en cosas más importantes que niveles.

`00:09:12` **SPEAKER_02** — Uriol, ¿tú en qué fase estás?

`00:09:13` **SPEAKER_06** — ¿Tú revisas el código? Sí. Sí, aún. Y voy intentando guiar al... O sea, antes que decíamos qué es TAC... Pero no escribes.

`00:09:26` **SPEAKER_02** — Mucho, muy poco.

`00:09:27` **SPEAKER_06** — O sea, últimamente estoy, esta semana toca OpenCode y es con el que uso. Y también estoy jugando con una app que se llama Handy, diría, que es similar a WhisperFlow, pero gratuita, que me la pasó Nacho. Básicamente le hablo al ordenador y le digo, haz esto. Y lo hace, mágicamente. O sea, tú hablas, vas por la casa. Bueno, de momento no estoy paseando, pero sí sería el siguiente paso. Hay otra app que se llama Paseo, que directamente te expone tus propios coding agents en tu ordenador, tienes acceso en el móvil y supongo que el nombre viene de eso. Mientras vas paseando, vas mirando qué van haciendo y le hablas y le dices, no, esto está mal y sigues paseando. ¿Tú, Edu? No sé cómo lo ves tú, lo que vayamos paseando mientras trabajamos. Yo lo veo fantástico.

`00:10:19` **SPEAKER_02** — O sea, mientras generemos ARR, que es mi monotema.

`00:10:26` **SPEAKER_03** — Yo en Factorio el reviso más código que nunca, seguramente, ¿no? Porque noto que soy el bottleneck. Hay PRs. ¿Tú eres el bottleneck de Factorio? Sí. O sea, uno de los bottlenecks. Sí, sí. Hay más PRs que nunca y hay gente que crea estas PRs y que ya no solo que no esté seguro de mergear, quieren que alguien la revise. No es tanto para decir si está correcto o no, es otra persona, además de yo, vio este código y entonces lo puedo mergear. No soy solo yo. Es como más el check que la revisión. O sea, lees código, ¿pero tú escribes código? No, no. O sea, casi no. O sea, llevo meses que no, o sea, desde diciembre no escribo código. Pero claro, escribir código que es escribir código, ¿no? O sea, no lo tecleo, pero el código que se genera yo lo tengo en la cabeza. O sea, me gusta todavía tener el control de cómo la gente está pensando y entonces, como entiendo cómo está pensando, sé qué código va a generar. No me hace falta leerlo para saber qué es el código correcto.

`00:11:21` **SPEAKER_02** — Pero seguramente no en la literalidad, ¿no?

`00:11:23` **SPEAKER_03** — No, pero las ideas están ahí. Las ideas, sí. Es que cuando reviso un APR, tampoco voy mirando línea por línea. Yo miro en diagonal y veo las ideas y digo, vale, esto me cuadra, esto no me cuadra. No soy más, va esta línea, no está correcta. Es más raro eso.

`00:11:36` **SPEAKER_05** — Pero me interesa también vuestra opinión en general, tú también, en ese sentido. ¿Qué tú revisas exactamente? Porque a mí, en mi caso personal, yo estoy enfocándome mucho más en interfaces, en conexiones entre módulos. Sí. Y también otras como... En maneras como verificar que todo funciona. En todos los tests, en Entwined, no sé qué. ¿Pero qué pasa dentro de este módulo?

`00:11:59` **SPEAKER_03** — A mí da igual. Sí, igual que tú. O sea, eso es lo que yo llamo la idea. El modelo del mundo que la gente o la persona hizo del problema, como lo expresó en términos, no en líneas de código que dicen exactamente cómo se resuelve el problema. Que el lenguaje creó el LLM para describir el problema y resolverlo en código.

`00:12:19` **SPEAKER_02** — Me voy a la sección. Miguel, ¿tú en qué fase estás?

`00:12:24` **SPEAKER_07** — Yo, muy parecido creo que a los demás, no escribo código directamente, sí que hago todo el código generado. ¿Ni una línea?

`00:12:33` **SPEAKER_02** — ¿Cómo? ¿Ni una línea?

`00:12:35` **SPEAKER_07** — Ni una línea.

`00:12:36` **SPEAKER_02** — ¿Desde hace meses? Desde hace meses, sí, sí.

`00:12:40` **SPEAKER_07** — Y no diría que sigo una progresión siempre creciente, creo que he tenido una regresión. Y quizá depende un poco del programa en el que estás. Yo escribía mucho, o sea, estaba a un nivel de abstracción superior hasta hace poco y he tenido una tarea donde he tenido que meterme un poco más de lo que antes me metía porque es una parte crítica de créditos y que tiene que ver con cómo cobramos y esa parte que me… Me ponía un poco nervioso, digamos, dejar a la hora. Míratelo bien, míratelo bien. Exacto. Entonces, en esa parte he vuelto a usar Cursor, por ejemplo, que es una cosa que había dejado completamente Cursor. ¿Y por qué? Cursor me permitía ver el código más directamente. O sea, me permitía hacer esos planes y iterar directamente más y verlo más y asegurarme más. Antes de Cursor, yo había dejado Cursor. No usaba Cursor, usaba Copilot, usaba otras herramientas. Y luego lo veía en GitHub, eso con los pull requests y tal. Pero ahora he vuelto para hacer esto a Cursor. Y bueno, para tener un pelín más de control, básicamente.

`00:13:36` **SPEAKER_02** — A ver, ¿de aquí quién utiliza Cursor?

`00:13:43` **SPEAKER_06** — Yo utilizo VS Code a veces en lugar de Cursor, porque si me espero a ver el código en GitHub, para mí el feedback loop es muy largo. A mí me gusta más ver lo que está haciendo para poder dar instrucciones de cómo corregir más rápidamente. Si ya veo que está yendo por un lugar que no me gusta, se lo puedo indicar. Lo tengo que probar, en teoría lo quería probar esta semana, pero he probado una cosa que se llama Crit, que en teoría te permite hacer esto de ir viendo en tu browser los cambios que va haciendo. Vas poniendo, puedes hacer como un pull request review, pero en live. Y se lo vas poniendo ahí y eso le pasa los comentarios al agent y hace steering. Y en teoría lo va haciendo y así es compatible con Open Code y todas las cosas y no hace falta algo tipo curso. Pero a mí las herramientas que son solo de terminal me faltan a veces de quiero ver por dónde se está yendo.

`00:14:40` **SPEAKER_02** — Vale. ¿Quién utiliza Cloud?

`00:14:45` **SPEAKER_03** — Aquí no, ¿eh? ¿Codex? No, yo uso OpenCode este mes con el modelo de GPT-4. Yo también.

`00:14:52` **SPEAKER_02** — ¿GPT 4? 5.4.

`00:14:54` **SPEAKER_03** — Ah, 5.4, vale. Vale, vale, vale.

`00:15:01` **SPEAKER_02** — Y a nivel de créditos, ¿cuánto consumís?

`00:15:06` **SPEAKER_08** — Yo estoy usando el CloudMax, no he acabado de gastarlo. ¿No? Me quedo en el max, me quedo al 70-75% compartiendo la suscripción entre personas.

`00:15:15` **SPEAKER_07** — ¿Se refiere que paga 200€ al mes? Sí, eso sí.

`00:15:18` **SPEAKER_08** — Pero en esa no soy capaz de gastarla. Entre varias personas no soy capaz, con Teams of Subagents, en múltiples terminales a la vez, no soy capaz.

`00:15:26` **SPEAKER_07** — ¿Y tú? Yo no, yo no, yo no, yo lo gasto todo lo que tengo. Yo gasto todo lo de la empresa y personales, lo gasto absolutamente todo, pero no he pagado los 200€ al mes de Hacker. Tengo, estoy suscrito a todo. Tengo OpenAI, los 20 euros al mes del PRO. Tengo el Eclot. Tengo Cursor también, el personal. O sea, lo gasto todo.

`00:15:50` **SPEAKER_02** — ¿Por qué el personal? Pues...

`00:15:53` **SPEAKER_07** — Sí, porque es que... Eso, o sea, gasto todos los tokens que puedo, básicamente.

`00:15:56` **SPEAKER_02** — Bueno, pero ¿aquí no podemos tener más tokens?

`00:15:58` **SPEAKER_05** — No, tenemos tokens, pero Cursor, por ejemplo, hemos parado a pagar. O sea, ahora os damos copiados para todo.

`00:16:03` **SPEAKER_02** — ¿Pero tokens no podemos tener más?

`00:16:05` **SPEAKER_05** — Tenemos tokens... No, no tenemos límite. No tenemos límite.

`00:16:07` **SPEAKER_02** — Ah, bueno, ¿entonces?

`00:16:09` **SPEAKER_07** — Bueno, o sea, sí, no tenemos límite, pero en Copailot como va como negativo, ¿no? O sea, llega un momento que llega a cero. Yo no sabía, la verdad, que no teníamos límite, porque en realidad... Cortamos, cortamos. Para eso están las tertulias. No, la verdad es que en Copailot tienes un contador y te llega a cero, ¿no? Entonces, siempre intentaba...

`00:16:28` **SPEAKER_05** — El descuento va negativo y es muy rojo.

`00:16:30` **SPEAKER_08** — Vale, vale. 1.500 por 100 y tal.

`00:16:32` **SPEAKER_07** — Vale, pues ya está. Entonces, llegará la factura.

`00:16:36` **SPEAKER_01** — ¿Tú, Adrià, cuánto quemas? Yo, bueno, varía, depende de los meses. Es verdad que cada vez quemas más y además ahora todas las grandes empresas están subsidiando el consumo de tokens. Por ejemplo, lo que les está pasando a Cursor es que ellos revenden tokens de otras empresas, de Antropic y de OpenAI, pero en cambio las empresas que tienen el modelo y que también tienen el producto de Kodi lo que pueden hacer es subsidiar los costes y últimamente han salido varios estudios de esto y por ejemplo Cloud Code está como subsidiando a 10 veces más lo que les cuesta realmente OpenAI.

`00:17:17` **SPEAKER_02** — Se ha discutido mucho y no tengo claro que al final la conclusión sea que se subsidía. Sí, sí, sí. 3X sí.

`00:17:23` **SPEAKER_05** — 3X. 1 o 3, sí. Por eso, si tú compras Max, y si tú comparas con el precio que tú vas a pagar por el token por API, tú tienes...

`00:17:35` **SPEAKER_02** — Pero no respecto a su coste. No, el coste no sabemos.

`00:17:37` **SPEAKER_05** — Respecto al crédito... El coste de la API versus...

`00:17:40` **SPEAKER_01** — Ah, bueno, ya. Y por eso ahora Cursor ha sacado su nuevo modelo, porque están en una posición muy mala, porque no pueden competir con Koster. Bueno, están en una posición mala porque dependen de los proveedores, que también son competidores suyos. Pero tú, ¿cuánto quemas? Yo va variando, pero unos 100 euros al mes entre suscripciones. Voy probando todo lo que está de moda. OpenAI, Cursor... Hay un meme de esto bastante popular en Twitter, que es la rueda. Cada vez que hay un release de un proveedor, todo el mundo se pasa... ¿Al nuevo? Sí, y vas cambiando. Depende de la semana.

`00:18:17` **SPEAKER_02** — Joan, tú eres PM. Sí. ¿Y qué haces aquí?

`00:18:20` **SPEAKER_00** — Pues buena pregunta. Yo también me lo pregunto y se me pregunta directamente.

`00:18:26` **SPEAKER_02** — No, no, mi pregunta es, mi pregunta es, ¿tú programas?

`00:18:30` **SPEAKER_00** — Depende de lo que tengamos por programar. O sea, ¿tiro PR? Sí. ¿Subo código? Sí. ¿Utilizo el código como herramienta para trabajar? Sí. ¿Los agentes para herramienta como trabajar? Sí, correcto. También, yo como me lo planteo, ¿no? Yo soy el Product Manager del LMS, ¿no? Del Learning Management System, y al final es un producto muy nuevo, y yo como si asumimos o si nos creemos esta idea, que el PM es el CEO de su producto, yo cuando miro a mi producto veo que el bottleneck número uno que tenemos es Code to Production, o sea, es un producto muy nuevo, yo tengo que competir con gente, con LMS modernos, con LMS legacy pero que llevan mogollón de features, yo no tengo features, no tengo cosas como muy básicas, table stakes, que le llamamos, entonces todo lo que podamos tirar, y tengo un equipo pequeño, esto es una ventaja para algunas cosas, pero para otras no, entonces todo lo que yo pueda hacer para sacar cosas nuevas al LMS...

`00:19:26` **SPEAKER_02** — O sea, tú ves que el cuello de botella es producción. Ahora mismo para el LMS seguro. Y que tú puedes ayudar. Sí. O sea, las dos cosas, ves que es esto y que tú puedes ayudar.

`00:19:34` **SPEAKER_00** — Claro, o sea, yo tengo ingenieros que necesitan estar en épicas más largas, más complejas, que yo no puedo hacer ni de broma, ¿no? Pero hay cosas pequeñas, yo sé, esta semana hemos resuelto tres bugs que los he hecho yo directamente, o cosas pequeñas que se pueden hacer que así les quito ese trabajo de context rot, pero de la persona, ¿no? En plan de, hostia, no puedo estar haciendo tres cosas a la vez, si lo puedo hacer yo y se lo quito de encima, mucho mejor. Clarísimo.

`00:19:59` **SPEAKER_08** — ¿Vale? Y, Jacob, dispara. Pequeñas, entre comillas. Tu, en concreto, eres un PM techy, ¿sabes? Te tienes PRs de 70, 75 archivos. O sea, no son, no estamos hablando de PRs de tres archivos, estoy tocando aquí un alto, ¿sabes? Son PRs introducidos. Luego hablamos, eso.

`00:20:16` **SPEAKER_00** — Cuando ellos hablan de, ahora tengo que revisar muchas PRs, yo soy el problema. Yo soy un poco, no, no.

`00:20:21` **SPEAKER_02** — Eso es lo que iba a preguntar. ¿Hay alguien que esté en contra de que el PM saque pull request? Aquí no se va a ofender nadie. Yo menos.

`00:20:31` **SPEAKER_06** — Yo lo único que estoy en contra es de que hagamos deploy o producción de código que nos va a traer problemas.

`00:20:37` **SPEAKER_02** — Hombre, pero a ver, ¿quién no está en contra de eso?

`00:20:40` **SPEAKER_06** — Ya, pero el otro día había un artículo, no me acuerdo cómo se llama, que el bottleneck ahora era toda la revisión y realmente es eso, porque a veces tengo la sensación de que quien produce ahora el código tiene que pensar menos o trabajar menos que la persona que lo está revisando. Porque como aún no tenemos un flujo de revisión tan automático...

`00:21:04` **SPEAKER_02** — Ese tema es muy interesante, porque... ¿Qué es pensar? ¿Pensar en qué? Porque hay muchas cosas a pensar cuando haces una pull request. Una es el problema a solucionar, que igual Joan tiene más conocimiento, porque tiene más contacto con el problema, que algunos de los ingenieros. Y la otra es cómo esta solución que estás planteando encaja en el ecosistema de un producto más grande. ¿No? Y esto son dos cosas a pensar.

`00:21:28` **SPEAKER_05** — Pero también token de responsabilidad. Sí, exacto. Si tú generas un montón de código y después, mira, alguien va a revisar esto y va a poner sus sellos de calidad y después deployamos. Pero claro, porque esta primera parte ahora es casi gratis. Pero revisar no. Sí, porque hay más stakes, hay más responsabilidad ahí. Por eso, ¿cómo hacemos este código?

`00:21:47` **SPEAKER_09** — Y además lo hemos invertido. O sea, la realidad es que hemos invertido un montón de tiempo en estandarizar y mejorar todo lo que va desde la ideación hasta la pull request, que es el primer paso antes de salir a producción. Y no hemos todavía invertido ese tiempo de calidad en la automatización de la revisión, que lo estamos haciendo ahora. Se llega un momento en que esa última validación, no te digo que sea todo 100% automático, el 100% de los casos, pero seguramente el 50, el 60, el 70, en cuestión de un mes, lo podremos automatizar. Y vosotros podéis invertir el tiempo en ese 5 o 10% que comentaba Edu, de revisar esos casos complejos.

`00:22:22` **SPEAKER_06** — Y el problema es saber cuál es el 5 o 10%. Sí, mi trabajo esta semana, se lo decía Ile, básicamente escribir todo lo que yo tengo en la cabeza cada vez que reviso las cosas en un documento y así no lo tengo que hacer yo y lo hace Copilot, en nuestro caso, revisando pull requests, porque si no, se lo decía el equipo el otro día, en nuestro caso de One, normalmente teníamos unos 30 pull requests pendientes de revisar. Esta semana ahora igual tenemos 150 o algo así, porque no damos abasto.

`00:22:52` **SPEAKER_02** — ¿Y esos son los PMs de Haciendo Por Recuerd?

`00:22:54` **SPEAKER_06** — Bueno, son 20 equipos de producto haciendo PR como loco.

`00:22:59` **SPEAKER_05** — Pero para mí es un parte, no es parte, es un trabajo de staff developer ahora. Es como, no podemos permitir más que es contexto tan importante, con toda experiencia y con todo esto. ángulo muy ancho de división de todo el ecosistema, vive solo en sus cabezas. Tenemos que extraer esto y ponerlo en un agente que después podemos multiplicar por todos los otros.

`00:23:19` **SPEAKER_03** — Ese es el 5%. Ya no es cómo resuelvo el problema, es cómo creo los boundaries alrededor para saber que todo el conjunto de soluciones posibles encaja en este boundary que yo he definido.

`00:23:32` **SPEAKER_02** — Yo soy un poco escéptico de esto. ¿Exista la capacidad de crear un revisor para cualquier cosa?

`00:23:38` **SPEAKER_06** — Para cualquier cosa, no. Si me saca la mitad del trabajo, yo estaría contento. 300 revisores. O sea, el 5 o 10 por ciento.

`00:23:47` **SPEAKER_02** — Pero, ¿y eso no es lo que ya es? O sea, ¿tú pones varios agentes a revisar? ¿Distintos? ¿Sin contexto? ¿Con contexto? ¿No? ¿Y los pones a revisar el pull request? ¿No encontrarán problemas? Con un conocimiento mucho más universal, ¿no? Y mucho más completo. Pero universal.

`00:24:03` **SPEAKER_09** — Tiene que ser el contexto de factorial, ¿no?

`00:24:04` **SPEAKER_05** — Problemas profundos, no. Es como, es más de este comentario que mira, tenemos 20 pull requests haciendo el mismo error, por eso, ¿cómo podemos crear una abstracción por encima? Esta gente no va a hacer nada.

`00:24:15` **SPEAKER_06** — El agent empieza con un pull request y acaba, y por eso me refería antes de que no hemos, nos falta este tooling de tener este contexto, esta memoria. El agent no se acuerda que ya ha revisado otro pull request que era casi igual, pero yo sí.

`00:24:28` **SPEAKER_02** — Bueno, sí se puede abordar, ¿eh?

`00:24:32` **SPEAKER_06** — Lo que dice Emilio, no tenemos el tooling aún de que haya una memoria de revisión de pull request, un historial. El tema no es solo el contexto de la memoria,

`00:24:42` **SPEAKER_09** — es el contexto de factorial. Porque aquí tenemos un equipo de staff, tenemos que darle esa capacidad a los agentes, a que tengan el conocimiento que tiene actualmente nuestro equipo. Y ese 5 o 10%, ese conocimiento que ellos no tienen realmente, que se enfrentan en la siguiente pull request. Y eso saldrá. Eso es lo que tenemos que revisar manualmente.

`00:25:03` **SPEAKER_02** — ¿Veis imposible la automatización total?

`00:25:08` **SPEAKER_07** — Yo no la veo imposible para nada. Yo creo que no conocemos los límites, es decir, que ahora mismo estamos probando cosas y toda la industria está probando cosas y estamos muy lejos de saber dónde está ese, lo que decía Edu, ese 10% que la AI no puede hacer. Yo no sé dónde está ese porcentaje. Es decir, yo creo que muchas veces cuando pones la lupa te das cuenta de que lo ha hecho mal porque tenía mal contexto, porque le faltaban cosas. Pero es muy difícil de poner la lupa y que te encuentres un caso en el que fundamentalmente no podría haberlo resuelto. Entonces, en ese sentido, es lo que decían ellos, de que falta tooling, falta muchas cosas y está todo muy verde.

`00:25:47` **SPEAKER_02** — ¿No pensáis que al humano le pasa un poco igual cuando hace un bug, cuando hace algún fallo? Es porque le falta contexto.

`00:25:53` **SPEAKER_06** — Por eso no todo el mundo es staff cuando empieza, porque no tienes el contexto de años de experiencia y ir acumulando y ir aprendiendo, que es la parte que creo que les falta a los agents de feedback. He revisado 10 pull requests que he aprendido en este tiempo. No digo que nuestros agents no aprendan nada. Simplemente van haciendo y ya está.

`00:26:15` **SPEAKER_00** — Aquí todos tenemos acceso a las mismas tools y al mismo teclado, pero es evidente que la calidad del código que genera mi agente, que es el mismo que el de cualquiera de los de aquí o un poco distinto, es mucho peor. Porque yo no le puedo dar el contexto adecuado, porque no tengo las ideas adecuadas, porque no tengo el conocimiento profundo que tiene todo el mundo que está aquí de la codebase, de cómo funciona el código. Puedo hacer mucho más de lo que hacía hace dos años, evidente, ¿no? Pero no puedo hacer lo que hace ninguno de ellos. Pero eso es lo que estamos intentando solucionar.

`00:26:46` **SPEAKER_09** — Esa parte ya la tengo bastante avanzada, ¿no? Con todo el tema de las Guidants, con la parte de Legend MD, Skills, más cerca del código, también la parte de los dominios, que vamos enriqueciendo. No es perfecto, ¿no? pero ahí hemos invertido bastante tiempo y la idea es que tú, una vez defines esa especificación, esa definición funcional del producto, pues a partir de ahí, hasta pull request, sea algo más o menos estándar en factorial, que importa un poco menos quién hace ese primer paso.

`00:27:16` **SPEAKER_02** — Porque otra cosa que estamos trabajando, y creo que también toda la industria está trabajando, es en la estandarización del PROM a través de specs. O sea, crear un lenguaje de specs que igual pueda hablar Joan y que tú puedes directamente definir qué es lo que esperas que se construya por un lenguaje concreto y que le aplicarán luego unas skills de desarrollo concretas que han hecho la gente más senior de la empresa y que es capaz de trasladar la spec en código.

`00:27:45` **SPEAKER_08** — También es verdad que siempre como que lo enfocamos a la parte de la ingeniería, pero el product manager tiene un montón de conocimiento en negocio para resolver el problema, el designer tiene un montón de conocimiento de cómo se resuelve ese problema a nivel de diseño, y normalmente estamos como pensando en las skills y en cómo las materializamos de la parte de la ingeniería para que los PMs la utilicen, pero también estamos intentando transicionar a que los PMs y los designers pongan su domain knowledge en skills para que los ingenieros puedan pivotar hacia negocio y hacia diseño, ¿sabes? Nada para un Staff Engineering Factorial de coger paper, pencil o cualquier cosa y hacer un diseño. Uno debería pararle, ¿sabes? Entonces, también necesitamos eso. Por ahí. Y yo creo que al final el 10% del que estamos hablando como que siempre se mueve, ¿no? Es decir, el 10% de hoy no es el 10% del año pasado. Siempre hemos resuelto el 0 al 90, ¿no? Estamos en el 0 al 90, estamos en el 0 al 90, pero siempre estamos en el 0 al 90. Porque el 10% en sí mismo no es el mismo que el 10% del año pasado. Movemos la capa de complejidad en la que nos abstraemos, Entonces resolvemos esa. Y nos quedamos ahí. Entonces nos movemos a la siguiente. Ah, vale, ya hemos resuelto este 10%. Y seguimos, y encontramos un nuevo 10%. Que no tiene nada que ver con el problema que resolvíamos antes.

`00:28:51` **SPEAKER_02** — Pero eso es la historia de la humanidad. Sí, claro.

`00:28:53` **SPEAKER_08** — O sea, no creo que sea... Exacto.

`00:28:55` **SPEAKER_02** — O sea, está haciendo un cambio muy concreto ahora, muy, muy

`00:28:58` **SPEAKER_08** — heavy, pero siempre nos ha ido pasando esto. Sí. Si evaluáramos, si dijéramos, creemos, hace dos años, creemos que vamos a resolver el 100% de lo que tenemos hoy como problema, decíamos no. Pero si evaluáramos hoy lo que era el 100% del problema antes, probablemente sea así.

`00:29:12` **SPEAKER_02** — ¿Oye, el cuello de botella, aparte de tú, de factoria, qué es? O sea, es porque si todo el mundo puede estar haciendo pull request, ¿no? O sea, entiendo que hacer el merge, o sea, la revisión de la pull request y llevarse este código a producción, esto es lo que es el cuello de botella, ¿no? Poder revisar todo este código.

`00:29:32` **SPEAKER_03** — Sí, ¿no? Totalmente. No es tanto el revisar, es asegurarse de que funciona. O sea, yo... Es el revisar, ¿no? No, porque tú puedes revisar algo y que luego no funcione.

`00:29:42` **SPEAKER_02** — No es el análisis sintáctico y ya está.

`00:29:44` **SPEAKER_03** — No, pero al final es un sello de yo, si algo falla, voy a ser yo el que lo va a arreglar. No es solo el revisar. O sea, tú cuando creas una PR, si lo crea un PM, Cuando eso falle en producción, va a tener que arreglarlo una persona. Si el PM no tiene las skills para arreglarlo... ¿Tú no lo vas a arreglar, no?

`00:30:05` **SPEAKER_00** — Depende. A ver, muchas cosas sí, claro. La idea es que sí. Aquí hay también una parte de responsabilidad de la gente que tira la PR. Al final... Yo he hecho algunas barbaridades muy grandes, que se han quedado en draft, por suerte. Pero luego, hablando con estos señores, quien sea, te dicen… Hombre, espérate un momento. Aprendes también a decir… ¿Qué entra dentro de mi scope? ¿Qué puedo hacer? ¿Qué no puedo hacer? hacerlo en PRs más pequeñas, aprendes a desarrollar de otro modo, pero aprendes qué es lo que se puede hacer, qué es lo que no se puede hacer y cómo lo vas a mantener también. Si falla el día de mañana yo tengo que entender lo suficiente lo que he hecho, no hace falta que yo entienda, yo no lo entiendo, cada línea de código que yo meto, pero sí entiendo las ideas clave de lo que estoy metiendo o debería entender las ideas clave de lo que estoy metiendo porque luego cuando le tenga que hacer traspaso a un ingeniero o lo tenga que arreglar yo, le pueda dar el contexto adecuado a la gente, ¿no? Digo, hostia, vale, no, falla porque hemos hecho esto, esto, esto y esto. Si falla esto, debe ser este punto. Si yo lo entiendo, puedo solucionarlo. Si no lo entiendo, no. Si tiro una PR y, bueno, y además es una irresponsabilidad tirar una PR, y decir, bueno, no sé, que la entienda otro, que la gestione otro y que la revise otro, que a la práctica lo que estoy haciendo es decirle a la otra persona, pues a Jacob, a Miguel, a Muriel, a quien sea, a Edu, a Atria, mira, o sea, hazme mi trabajo, que yo estoy intentando hacer, que no es tu prioridad, pero si es la mía, hazlo tú. Esto no puede ser. No, también.

`00:31:28` **SPEAKER_02** — Ya, pero la práctica acaba siendo un poco así, ¿no?

`00:31:30` **SPEAKER_00** — Bueno, esto lo tenemos que solucionar. Y esto es una cosa que tenemos que aprender. La gente que estamos, que no somos ingenieros, que estamos tirando PRs, tenemos que asumir esta responsabilidad también.

`00:31:38` **SPEAKER_05** — Por eso, para mí, un cuello de batalla no es revisión per se, es un síntoma. Pero el problema es que no tenemos a veces tan claro qué es bueno, qué es malo. Esas definiciones de estándar, que un par de tocarías, Miguel, es así. Pero no es solo skills, sino solo agents. Es también todas las abstracciones, todas las infraestructuras, todas estas cosas de framework que normalmente gente está haciendo porque agents está aprendiendo de datos de contexto de texto, pero también de otro código que está por ahí. Y si ven un montón de cosas no tan estructuradas, van a repetir esas cosas no tan estructuradas. Por eso voy a repetir, el trabajo de un ingeniero ahora es ver esos patrones y después hacer esto más fácil para una gente encontrar un camino correcto. Sí, claro. Revisión es una parte como tú sacas esto.

`00:32:24` **SPEAKER_08** — Pero también el PM es como el nuevo Junior, ¿no? Es decir, hace hasta donde... ¿No? Mi sensación, ¿eh? El PM hace hasta donde le llega la comprensión de lo que puede hacer tanto del problema como del código en el que se materializa. Lo lee y dice, high level esto está guay. ¿Sabes? El junior igual. Y luego tú lo revisas y haces un back and forth. Pero nuestra responsabilidad es un acompañamiento para que la siguiente PR que meta el PM, igual que si fuera un junior, sea mejor, sea más atómica, sea más idiomática. Yo creo que es

`00:32:56` **SPEAKER_07** — que últimamente todos volvemos a ser juniors. O sea, no solo el PM. Es que se dice, por ejemplo, que los LLM son como junior programmers, se dice que los PIN son juniors, pero que nosotros también somos juniors porque estamos en esta transición de software tradicional a software 2.0 donde son PROMs y nosotros no llevamos 10 años haciendo PROMs, llevamos 10 años haciendo software con código, entonces nosotros tampoco somos tan buenos necesariamente haciendo PROMs, entonces también está la pregunta de quién nos revisa a nosotros. Es decir, al final, también somos juniors nosotros. De hecho, ¿sabes qué?

`00:33:29` **SPEAKER_09** — Hoy un junior es un disruptor. O sea, el concepto de junior que tú explicas, creo que es el concepto equivocado. Es el concepto de hace 10 años. El de hoy es la persona que viene a mover a equipos más señores de ingeniería.

`00:33:44` **SPEAKER_02** — Depende del junior, ¿eh? Pero sí, sí, el bueno. El que queremos contratar seguro.

`00:33:54` **SPEAKER_09** — Totalmente, pero hay gente que es native. Esta gente ya lleva dos años trabajando con esto.

`00:33:59` **SPEAKER_02** — Este para mí es el mayor challenge que le haría a Oriol y a Edu. Vosotros valoráis mucho los años de experiencia, y lo entiendo, porque al final hay una serie de conceptos que hay que entender, cómo funciona Internet, cómo funcionan los protocolos HTTP, cómo funcionan las diferentes capas de una aplicación, las bases de datos. O sea, son cosas que requieren tiempo. Sin embargo, lo que dice Miguel, ha cambiado tanto el mundo que una persona que nace ya en este mundo y se mueve de forma natural en este mundo, igual no tiene todos los strings attached de esa sensación de control. Es como una persona que era muy senior en Assembler. Dices, está muy bien que seas muy bueno en Assembler, tío, pero es que estamos haciendo rubi aquí, ¿sabes? Entonces, dónde colocar el puntero o la memoria o no sé qué, igual no es tan importante como diseñar patrones de software a un nivel mucho más alto. Entonces, la experiencia tan buena y tantos años en alguna cosa, igual no te sirve en otra cosa. Y la persona que nace ya directamente en este nuevo patrón, Pero ahora le pasaré el micrófono. Este nuevo patrón, pues igual esto no le sirve. Es un challenge que os dejo aquí. El junior con AI. El junior proactivo, motivado, autodidacta, que lleva programando también desde los 14 años, como todos los de aquí, pero que no tiene vuestra experiencia.

`00:35:17` **SPEAKER_06** — Yo creo que se ha repedido muchas veces el problema. Nunca había sido generar código. El problema es saber qué código escribir y precisamente detectar esos patrones, ver abstracciones, pensar en sistemas. Ese es el problema. El generar el código, pues ahora tenemos una manera increíblemente rápida de generar código y no tenemos que escribirlo nosotros.

`00:35:38` **SPEAKER_02** — Pero los sistemas cambian, ojo, que los sistemas cambian.

`00:35:41` **SPEAKER_09** — La velocidad de iteración. El problema no era generar código, pero la capacidad de iteración que tienes ahora, el feedback loop... ¿Cuántas veces eres capaz de iterar en una semana? ¿Cuántas veces eres capaz de hacerlo hace tres años?

`00:35:56` **SPEAKER_06** — Te lo compro, pero lo que me refiero es, lo que valora los años de experiencia es no saber que el standard library de Ruby, pues vale, felicidades. irás más rápido antes, pero lo interesante es pensar en sistemas y eso es más... seguramente ahora se aprende mucho más rápido, o sea, lo que antes igual tardaba 10 años, pues ahora en dos quizá o tres lo puedes aprender. Es la diferencia.

`00:36:20` **SPEAKER_02** — Sí, pero lo que te quiero decir es que los sistemas ahora son igual otro tipo de sistemas, son ecosistemas, digamos, ¿no? Más que cada módulo, cada clase, qué hacen... ¿Te preocupa más? ¿Cuáles son las lógicas de negocio? ¿Cómo se comunican entre ellas?

`00:36:33` **SPEAKER_03** — Eso ya era así antes. Yo nunca revisaba línea por línea. Antes de la AI no revisaba línea por línea. Tú revisas módulos, abstracciones, ideas...

`00:36:44` **SPEAKER_06** — Y Lea decía de explicar cómo revisamos puls recuestos. No se explica. Yo lo leo así en diagonal y a veces leyendo ves algo raro. Y cuando ves algo raro sí que te pones a leer exactamente qué es eso. Pero nunca hemos... Si tuviéramos que revisar todo línea por línea, estaríamos...

`00:37:02` **SPEAKER_02** — Y ahora esa intuición de leer en diagonal y tal, conviértela en skill. Good luck.

`00:37:10` **SPEAKER_05** — Al final, si tú piensas bien y si tú, pero tienes que gastar tokens mentales, toques mentales para extraer esto a un skill, porque es un para ti es un raro que tú estás encontrando a un.

`00:37:21` **SPEAKER_02** — Esto concretamente, pero luego la otra cosa.

`00:37:23` **SPEAKER_05** — Pero vale, pero es como tú estás.

`00:37:25` **SPEAKER_02** — Al final tu cerebro es un LLM que está infiriendo.

`00:37:28` **SPEAKER_05** — Sí, sí, sí, pero al final el valor de esta experiencia, este contexto es mucho contexto. Es el valor de tu experiencia. ¿Cómo tú lo piensas? Es un contexto para mí.

`00:37:37` **SPEAKER_02** — De toda tu vida, ¿eh? Escribe un markdown con tu vida. Bueno, hacemos mucho compaction. A lo largo de los años hacemos mucho compaction.

`00:37:46` **SPEAKER_06** — Igual hay que cobrar comisión en las skills, entonces. Lo que es intelectual.

`00:37:52` **SPEAKER_02** — Hay gente que habla de eso.

`00:37:53` **SPEAKER_03** — Y luego no es tu vida. Yo a veces veo una PR y digo, vale, esta que la revisa Oriol también. Porque hay cosas. No te desbloqueas. Hay cosas que yo sé que no llego hasta ahí. O sea, quiero que lo vea Oriol, ¿no? Con Agente, no. Los agentes sueltos son iguales. No hacen este handover de quiero que la revise un humano.

`00:38:13` **SPEAKER_09** — Les ponemos un SoulMD y llegas hasta aquí tú y ya está. También. Entonces, yo os hago una pregunta un poco más... desde el punto de vista un poco polémico dentro del mundo ingeniería. Si el junior aporta esta capacidad de disrupción dentro del ecosistema y el staff proporciona esta parte de conocimientos, fundamentos, visión global, transversal, abstracción, guidance para las escrituras y demás, ¿Dónde queda el espectro de mids y seniors?

`00:38:49` **SPEAKER_03** — O sea, ¿cuál es el reto que tienen ellos ahora en los próximos años? Hay una base, ¿no? O sea, ¿por qué un niño de 8 años no puede escribir una fitura bien factorial? O sea...

`00:38:58` **SPEAKER_02** — Espera, espera. Va a escribir un prompt y va a generar un

`00:39:01` **SPEAKER_03** — código que va a tener sentido y seguramente funcione. O sea, ¿qué es lo que aporta un senior, un PM, un designer?

`00:39:08` **SPEAKER_09** — No es lo que aporta, es ¿cuál es su lugar en los próximos años? O sea, porque como está evolucionando todo, van a tener que evolucionar muy rápido. para que aportar o en la primera línea, que es esa parte de irrupción, o en la parte de los fundamentos. Y ahora mismo se quedan en un área más gris. El problema no es hoy, el problema es un año y medio, dos años. Hay gente que tiene que crecer muy rápido.

`00:39:32` **SPEAKER_05** — Pero voy a hacer también un challenge que no es solo de casa de rol, que tú tienes juniors disruptores, staffs, haciendo mucho pensamiento. Yo he visto personas por todos los lados, diferentes personas.

`00:39:45` **SPEAKER_02** — He visto juniors generando un valor brutal y staffs, bueno, no tanto.

`00:39:52` **SPEAKER_09** — Pero, por otra parte, hay staffs que han generado un valor brutal.

`00:39:54` **SPEAKER_07** — Es decir, el creador de Cloud Code, ¿no? No es staff, es más que staff. Y fue él el que creó, no fue un junior. No fue un junior el que lo hizo. ¿Por qué no fue un junior?

`00:40:13` **SPEAKER_05** — Por eso estamos diciendo que depende del personal, que tú no puedes poner solo por rol. Claro, pero es que yo creo que…

`00:40:18` **SPEAKER_02** — Es decir, que si tú sumas motivación, energía, que a veces la gente de 20 años quiere que al menos sea una gente apasionada, energía, motivación, actitud a tope.

`00:40:28` **SPEAKER_03** — No siempre es así, entonces es un problema. Pero un niño también tiene eso.

`00:40:32` **SPEAKER_00** — A ver, yo ahora voy a ser un poco así, porque yo es que vengo del mundo de la educación, justamente, y de hecho en mi última empresa, donde yo trabajaba en una startup en Silicon Valley, es verdad que era un proyecto Greenfield, pero era una comunidad barra clases etcétera para homeschoolers que, como todo, hay un abanico gigante. Contratamos a un chaval de 10 años. O sea, como junior de como quiera. No tenía título. No tenía título. Y sacaba features a producción. No van broma.

`00:41:10` **SPEAKER_03** — Y features no menores. Está demostrado que, conforme vas madurando, vas perdiendo creatividad. La lógica te lleva a que un niño de 8 años va a pensar… Pero si aporte valor. ¿Por qué no? Ahí voy ¿no? ¿Por qué no? ¿Por qué no? Más allá de la legalidad. Temas menores.

`00:41:27` **SPEAKER_02** — ¿Y el staff, el niño de 10 años?

`00:41:30` **SPEAKER_00** — Claramente no. Pero trabajando codo con codo con nuestro CTO, pues sacaba features a producción solo. Un niño de 10 años, un niño excepcional, evidentemente, ¿no? Pero sí, claro, evidente, es posible si hay la motivación y con el tooling. Este niño no habría escrito o tal, pero te hacía un debugging que no lo he hecho yo, ni algunos ingenieros, mid o lo que sea, que no he visto yo hacerlos. No, lo puse exactamente por esto, porque lo que aporta.

`00:42:04` **SPEAKER_03** — Tienes que ver cuál es el valor diferencial que aporta. Si es creatividad, dos o un niño aporta creatividad.

`00:42:09` **SPEAKER_02** — Es que hay grandes escritores, grandes científicos, grandes todo, que han creado su obra mayor con 20 años. Y luego no han hecho nada. O sea, que una cosa no implica la otra. Sí, pero en general...

`00:42:23` **SPEAKER_09** — En general la experiencia sirve. Sí, claro que sí. Pero al mismo tiempo te va generando una serie de restricciones, ¿no? Por el contexto. Bueno, te va volviendo

`00:42:31` **SPEAKER_02** — más conservador, igual menos creativo. Sabes más lo que no funciona. Tienes más miedo. Todo esto puede ser.

`00:42:38` **SPEAKER_06** — Exactamente. Eso me refiero a que es, en general, comportamiento humano. Más faltaría si los jóvenes no están haciendo disrupción y liando la parda. Es su función. Si no, no sé por qué.

`00:42:50` **SPEAKER_02** — ¿Y tu función es revisarles las veces?

`00:42:53` **SPEAKER_06** — No, mi función es quedarme mirando y decir, bueno, pues ya se me entera la hostia. No pasa nada. Así se aprende como todos. Pero al final también lo de ser disruptivo, yo creo que es más una actitud que una cosa de edad. Obviamente afecta la edad. pero creo que va más con la energía. Igual cuando eres joven puedes ser disruptivo en 10 cosas a la vez y yo ahora pues con 2 yo también estoy contento. Hombre, aquí hay mucha gente disruptiva. Ah, eso es un aparente interesante. Que no son juniors, ¿no? Exacto, sí, sí.

`00:43:21` **SPEAKER_09** — En estos momentos aquí, ¿no? Exacto. ¿Qué? Que hay mucha gente disruptiva aquí que no son juniors. No, claro.

`00:43:27` **SPEAKER_02** — Pues creo que es más una actitud. En estas mesas, concretamente, también, por ejemplo. ¿Tú quieres decir algo?

`00:43:32` **SPEAKER_07** — Sí, que una parte interesante de lo que decías, Uriol, que a lo mejor el kuye botellao ahora es más la capacidad que tenemos de paralizar como humanos y como individuos. Yo lo veo a veces que influye mucho cómo capaz soy de hacer dos cosas a la vez, tres cosas a la vez, y cómo me voy entrenando para ser capaz de hacer más cosas y mover un poco la aguja ahí. Porque es difícil, porque antes estábamos acostumbrados a unos límites distintos. Y entonces ese quizá sería el cuello botella.

`00:44:01` **SPEAKER_02** — Ah, esto es interesante. O sea, hemos hablado del cuello de botella, la revisión del código. Aunque vamos automatizándolo y cada día vamos mejorando en eso. Otro es la capacidad para realizar, ¿no? Hacer varias... La pantalla esa del... Steinberger, ¿no? Del Cloud Code. Ah, sí, el de Cloud Code. Open Cloud. que tiene como 50 pantallas ahí y está haciendo como un millón de cosas a la vez. Y yo, con un cuarto de estas pantallas, ya me perdería. Entonces, la capacidad de paralizar. Y lo otro es el tiempo que tarda el modelo en darte una respuesta. Porque hay muchas veces que estamos así. Sí.

`00:44:37` **SPEAKER_06** — Bueno, aprovechas para lanzar otra cosa. O para caminar. O para pasear. Es el momento de paralizar.

`00:44:43` **SPEAKER_07** — Es el momento de paralizar. Es una oportunidad para paralizar. Que si no la haces, pierdes potencialmente. O sea, es una feature el tiempo.

`00:44:50` **SPEAKER_02** — El tiempo que tarda es una feature. Es algo bueno.

`00:44:52` **SPEAKER_07** — No, no, no. Pero es una oportunidad para paralizar. Que si no paralizas, estás dejando productividad en la mesa.

`00:44:57` **SPEAKER_02** — ¿Y no sentís que lleváis la neurona al máximo en estos momentos? O sea, que estamos viendo la capacidad del ser humano ahí al límite, al límite. Mientras tenemos todos estos procesos en paralelo. Porque te haces mucho focus shift.

`00:45:12` **SPEAKER_05** — Si estamos hablando de paralelizar a gente, significa que hay n features o n ideas que tú estás atacando en paralelo. Por eso, si quieres hacer esto bien, tú tienes que como mínimo tener esta imagen en tu cabeza. ¿A dónde vamos? ¿Cuál es la idea? ¿Cuáles son límites? Si multiplicas por 3 o 4, mira, tú vas al límite. Y después tú tienes esto en tu móvil. Tú también estás paseando y es que tienes.

`00:45:33` **SPEAKER_02** — ¿Quién tiene el móvil aquí, el dispatch este? ¿Sí? No, dispase que he ofrengado. Otra cosa, pero no, sí. Con Ilia normalmente ya lo ves distraído y cuando habla con Ilia está como mil cosas, está pensando mucho, pero es que ahora está con el puto móvil con varias pantallas en paralelo y es que no puede tener una conversación con foco, ¿no? O sea, todo eso os pasa un poco lo mismo. Es genial eso.

`00:45:54` **SPEAKER_06** — Esto del foco, la cosa esta mística del programador de que estás en el flow y estás ultra concentrado y no te das cuenta de que han pasado tres horas. Diría que ha desaparecido.

`00:46:08` **SPEAKER_08** — A mí me desaparecen las seis horas. Lo que pasa es que en lugar de estar...

`00:46:11` **SPEAKER_06** — O sea, el flow es paralelizado. Sí, exacto. Pero no estás en un problema durante mucho rato. Es constantemente ir saltando de problemas.

`00:46:20` **SPEAKER_05** — Y también tienes otro nivel de abstracción. A veces yo saque ideas cuando estoy paseando. En el background tú estás pensando de cosas y tu agente está verificando tu idea.

`00:46:32` **SPEAKER_06** — Sí, sí, normalmente las mejores ideas no son cuando estás en el ordenador, es cuando estás paseando o haciendo otras cosas.

`00:46:39` **SPEAKER_00** — ¿Cuántos de aquí sois jugadores o ex jugadores del Starcraft o de Factorio? No es el mismo flow. O sea, para mí es el mismo flow exacto que cuando estabas controlando 20 cosas a la vez o en factorio, que estás pensando todo el rato en cómo automatizo eso, cuándo se me acaba de construir lo otro, por lo tanto voy a la siguiente base, cambio de planeta, cambio de… O sea, para mí, cuando tengo 5 tabs o… 10 tabs abiertas de Py o de Codex o lo que sea, mi cabeza está en el mismo sitio.

`00:47:08` **SPEAKER_07** — Bueno, de hecho existe esa vista de poder jugar como al StarCraft si estás controlando agentes.

`00:47:14` **SPEAKER_00** — No lo he probado todavía. Yo no lo he probado, pero me parece que sí que existe. Es la leche. Para mí, yo que no he tenido este feeling de programar Deep no sé cuántas horas, sí que lo he tenido en el StarCraft o en el Factorio o lo que sea.

`00:47:26` **SPEAKER_02** — Gastown no es un poco eso.

`00:47:28` **SPEAKER_03** — Es lo contrario, justo. Es una sola tarea y tener muchos agentes que son autónomos, que necesitan prompt continuo, que ya funcionan durante horas solucionando este problema. Tú le dices, incrementa el MRR de factorial a 50 millones, le metes como prompt y lo tienes ahí continuamente haciendo experimentos y haciendo features. Es la idea, ¿no? Es una fact, es una... O sea, ya se va a dar el sur...

`00:47:56` **SPEAKER_02** — Me hace gracia porque vosotros os descojonáis mucho de mi visión de la RR, que yo lo entiendo, lo entiendo. Es nuestra función. No, no, no, pero es que aquí el tema de cuando pensáis en pensar el problema... Lo que muchas veces no le da tanta importancia a vosotros es de dónde viene esta tarea, el por qué estamos haciendo todo este motion de trabajo, este dominio, este producto, ¿no? O sea, ¿por qué lo estamos haciendo? Y al final es, alguien tiene que hacer esto, ¿no? Que es lo que hace Joan. va a haber gente, va a haber clientes, se genera una hipótesis, hace un proceso parecido en otro dominio de problemática y que al final tiene que acabar en solucionar un problema. ¿Y cómo lo medimos? ¿Cuál es el heurístico? En ARR. Pero lo importante realmente no es el ARR, lo importante es que estamos solucionando problemas a peña y que no estamos en nuestra cueva ahí creyéndonos nuestras tecnologías y estar todo el día jugando sin que sirva para algo. El concepto de servir es tan importante como el concepto de que no rompa la abstracción, o que no duplique no sé qué, o que no, no sé, ¿sabes? Y a veces no le damos tanta importancia a esto. No, pero aquí estamos de acuerdo todos contigo, ¿no? Bueno, no lo sé, ¿eh? No lo sé. Mucha coña me metéis con el tema de la RR.

`00:49:09` **SPEAKER_06** — Bueno, pero es fácil, pero al final yo creo que... Ya lo sé. ...todos los ingenieros lo que te gusta es resolver problemas. Claro.

`00:49:17` **SPEAKER_02** — Claro, pero ¿qué tipo de problema? ¿Qué tipo de problema? O sea, porque ¿el problema cuál es? El problema es construir algo, pero ¿ya alguien ha decidido que hay que construir algo? O el problema es previo a construir algo.

`00:49:29` **SPEAKER_06** — Para mí, la mejor manera... Siempre lo que quiero es no trabajar. Con lo cual, no trabajar me refiero a cómo poder solucionar este problema con el mínimo esfuerzo. Y ya está. Es otro tipo de problema. Para mí el problema es

`00:49:43` **SPEAKER_08** — dónde le duele al cliente. Y en febrero el cogemos y contratamos a un montón de product engineers y por eso pivotar. Yo vengo de abogado de los PMs, oye. Por eso pivotar y que los PMs programen es la hostia. Porque están todo el día con el cliente. Yo espero que resolvamos el botín de revisar para a partir del mes que viene que tengamos a todos los ingenieros juntándose con clientes. Y diseñarlo también, ¿sabes?

`00:50:05` **SPEAKER_06** — No, pues eso no cambia la otra. Por ejemplo, en Expense, es que a Bernardo, Helio o Miguel les pasa. El problema es que hay que controlar cuántas cosas se gastan y que la gente no se pase. La solución mala es que lo aprueben. Porque ya es solucionado. Ahora ellos van en el inbox, tiene chorrocientas mil cosas ahí pendientes de aprobar y no le ha solucionado el problema.

`00:50:34` **SPEAKER_08** — Claro, pero es que no es una solución, ¿cuál es el problema?

`00:50:37` **SPEAKER_06** — A eso me refiero con no trabajar.

`00:50:41` **SPEAKER_02** — Pero es más complicado que eso, es más complicado. Puedes decir que lo aprueben, vale. Igual está de acuerdo el CFO. de la empresa, porque dice, fricción, fricción, van a gastar menos, ¿sabes? O igual es diferente si hablas con el manager o con el CEO o con el, ¿sabes? Al final es un sistema también la empresa. Y tú tienes que mirártelo desde arriba y pensar, a ver, ¿cómo generamos valor en todo este sistema que más o menos deje contentos a todo el mundo y que al final sea un net positive, ¿no? Y eso es lo que hace Joan. O sea, y al final tiene que ser un net positive porque si no es un net positive, nadie va a pagar por ello, ¿no?

`00:51:17` **SPEAKER_06** — Pero a lo que me refiero es que un ingeniero que no tiene esta vista para mí no es un buen ingeniero.

`00:51:23` **SPEAKER_02** — Pero no está expuesto el ingeniero a este tipo de problema. El ingeniero parte de que alguien ha dicho que hay que construir esto. Y entonces dice, vale, hay que construir esto. Si partimos de aquí estamos mal.

`00:51:36` **SPEAKER_00** — Los equipos de producto deberíamos funcionar mucho más juntos. Hoy hemos hecho un meeting, mi equipo, exactamente de esto. He dicho, oye, basta ya. A mí me dicen, yo implemento. El producto es nuestro Y aquí contribuimos todos, no puede ser que mi cerebro o el del engineering manager o el de la designer valga más que el de todos juntos. Eso es el mundo ideal y

`00:52:01` **SPEAKER_02** — es la realidad de muchos equipos de factorial, pero también hay equipos que no. Y en cualquier caso, siempre pasa que el ingeniero está menos expuesto. De una forma obvia y natural, va a estar menos expuesto al problema. Entonces va a pasar un momento que el PM o quien sea que está cerca del mercado y se da cuenta que, ostras, esto ya no es una solución, y va a volver y va a decir, ¿sabes qué? Esto no. Y algún ingeniero, no digo los de esta mesa, pero algún ingeniero va a decir, joder, me han vuelto a cambiar lo que tengo que hacer otra vez. Me han vuelto a cambiar el mundo otra vez. Y esta frustración de ir encontrando el problema, construir lo mínimo para validar este proceso iterativo, pues es la magia.

`00:52:39` **SPEAKER_05** — ¿O va a pasar otra cosa? ¿Qué PM va ahora a tener claro quién era? Si esto genera tanto frustración, porque yo no puedo generar lo mismo con CodeCode o con otra herramienta. Está fantástico. Sí, porque en algún momento la pregunta es, ¿y por qué necesito este ingeniero? Si no me importa nada excepto tocar código. Superpositivo.

`00:52:56` **SPEAKER_07** — 100%. Pero el tema es que también la oportunidad, yo creo que también es que tú como ingeniero que tiene un pie siendo PM, también tienes muchas oportunidades porque tú cuando vas a hablar con un cliente ves lo que es inmediatamente más fácil de hacer y muchas veces es la diferencia entre ser capaz de ir a mercado en una semana o dos semanas versus un año. El PM no lo sabe. El PM no lo sabe y es muy difícil valorar todos esos detalles. Entonces, muchas veces, como programador o como persona que también tiene una parte técnica, tenemos una oportunidad enorme yendo al mercado para escoger un roadmap que al final es un camino súper óptimo, que nos lleva muy rápido al mercado, muy rápido a RR y que triunfa mucho más que una persona que llega y dice, ya, pero yo tengo que preguntarle a alguien cuánto se tarda en hacer esto. Y cada vez que te quieres... Ese ciclo es muy largo. Cada vez que te quieres mover algo y deas algo, tienes que preguntarle a alguien y tienes que asegurarte que esa persona entiende exactamente lo que le estás diciendo. Ese ciclo es larguísimo y es muy ineficiente. Entonces, en cambio, si tú como programador es capaz de ir al mercado y hacer esas preguntas, si te das cuenta y tienes la intuición para preguntar ciertas cosas, para saber que esto es muy fácil de hacer, le voy a preguntar y si esto resulta que es algo que es muy interesante, se van a juntar dos cosas, va a ser una conjunción de factores que me va a dar una oportunidad en el mercado.

`00:54:24` **SPEAKER_09** — Estamos hablando siempre de cómo parece que el ingeniero cada vez tiene menos relevancia y yo la verdad que lo puedo mirar de la otra forma porque hablamos de agentes, no hablamos de agentes que son programadores, hablamos de agentes que pueden hacer cualquier rol. En ese mundo en el que también puede pasar lo mismo con el otro rol, con el del PM. Yo creo que cada vez más Lo que importa son esas skills de las personas. Y como nos complementamos, como un equipo, va a encontrar valor. Y no tanto la skill concreta, la más detallada. Esa búsqueda de valor, para mí, es lo que todavía hace esto. Tú también estás en el Speederman, ¿no?

`00:55:00` **SPEAKER_00** — Donde el designer, el PM y el engineer están en plan, I don't need you anymore. Pues sí, pues un poco sí. Y a la par de quien, para mí, el perfil que emerge de aquí es un perfil mucho más polivalente. Un perfil de, no sé, le podemos llamar builder, me da igual, ¿no? Product maker, que tenía más años. Product maker, sí, ¿no? Un perfil mucho más polivalente. Que creo que es la clave. Los teams interesantes siempre han sido estos.

`00:55:21` **SPEAKER_06** — A lo que iba antes es, ahora hemos aplicado AI mucho en la parte de generar código, pero es lo que dice Miguel, ¿por qué no le pasamos las transcripciones de todos los account managers con varios clientes de la misma industria?

`00:55:36` **SPEAKER_08** — Y a partir de

`00:55:37` **SPEAKER_06** — aquí, podemos facilitar el trabajo de Joan, porque en lugar de tener que estar mirando ir a 10 reuniones con todos los account managers o leer los transcripts, pues hago que un agent especializado en encontrar... Estaba Leria haciendo esto. Esto lo tengo yo hecho. Te hemos enfocado mucho a la parte de programación, pero eso es que aplica a todo.

`00:56:02` **SPEAKER_02** — Y una reflexión que me gustaría haceros, porque aquí estamos hablando de construir código con agentes. Hasta ahora casi todo lo que hemos estado hablando es construir código con agentes. Pero claro, construir código sigue siendo el paradigma antiguo. desde mi punto de vista, ¿vale? Que esto me diréis... Pues bueno, dentro de un año igual. Yo creo que en el punto en el que estamos ahora es en construir AI as a service. Es decir, en facilitar la AI y llevarla cerca de nuestros clientes. De forma que ya no es tan relevante igual escribir código, sino crear un ecosistema donde el que escribe el código es nuestro cliente. Al vuelo. ¿Y por qué quiere escribir código? Bueno, normalmente los clientes lo que quieren es escribir más o menos. Me voy a explicar mejor, porque no me estoy explicando. No es que quiera escribir código, es que quiere resolver su problema. Y su problema es una casuística del long tail infinito de problemas que existe en el mundo. Entonces, el problema del código en general que tiene es que como es determinístico, como es un if-then-else, tienes que tener el if, tienes que tener la casuística considerada a priori. Reconocida. Claro, entonces esto te limita, porque implica, como ingeniero, pensar en todos los problemas del mundo. Y ya no solo los problemas, sino cómo construirlos y cómo adaptarlos en las abstracciones, todo lo que hemos dicho. Vale, ahora imagínate que nosotros, que es lo que estamos haciendo en Factorial, no sé por qué te sorprende, hacemos una IaaS service de forma que el cliente, por ejemplo, escribe código, no en lenguaje de código, sino en Policies, por ejemplo, que es la abstracción que tenemos en Factorial, en un lenguaje pseudocódico o directamente, absolutamente, lenguaje natural, con ciertas restricciones, donde esto se convierte al vuelo en tiempo de ejecución en código. Y esto es otro paradigma. Esto es lo que estoy viendo en mi observación, hablando con muchos ingenieros, es que cuesta mucho ceder este control a una gente que va luego a escribir el código por nosotros. ¿Cómo lo veis esto, o no? ¿O estoy diciendo tonterías?

`00:58:08` **SPEAKER_06** — No, yo creo que no, que tiene sentido y hace unos días o semanas que pienso que ahora lo importante que tenemos que invertir no es tanto en hacer features o cosas así, sino en cosas que sean building blocks, cosas core, para que para precisamente hacer esto, que alguien, bueno, alguien no, un agent puede componer una interfaz, una solución con todas, es como, mira, aquí tienes todo un paquete de herramientas que te damos, espabilate para solucionar los problemas del usuario. O sea, que ya no tiene sentido muchas veces hacer una pantalla con, yo he decidido que aquí hay un listado de empleados que cuando le das a este botón se te abre un side panel y te muestra esta información. Pero es muy difícil que un agent pueda hacer una pantalla autogenerada sin unos componentes, por decirlo de alguna manera.

`00:59:01` **SPEAKER_05** — y no solo componentes, sin este entendimiento muy claro de qué hay detrás de este dato, de este componente, de todo.

`00:59:08` **SPEAKER_03** — Y coherencia, porque no te vale que te vayas a una página y tenga una pinta, te vayas a la siguiente y se ve una aplicación distinta, y entras mañana y se ve una aplicación distinta otra vez, ¿no? Coherencia visual, de experiencia, ¿no?

`00:59:18` **SPEAKER_02** — Sí. Del design system, los componentes pensados previamente. Miguel, ¿tú qué piensas de esto?

`00:59:26` **SPEAKER_07** — Yo sí, o sea, yo creo que ahí se mezclan dos cosas. Yo creo que una es la transición de software 1.0, creo que Carpazzi lo dijo esto, software a software 2.0, creo que lo llamó así, que es la transición de cuando tienes un software que es un poco distinto a lo que decías, que está ejecutando prompts en lugar de ejecutar código. estás ejecutando prompts todo el rato. Y eso puede ser una transformación interna en una empresa, que pasa de ejecutar código a ejecutar prompts, versus vender este servicio donde tienes ese nivel de customización y tú escribes los prompts para ofrecer ese servicio y es muy customizable y tal. Las dos cosas, o sea, lo que estamos haciendo en Factorial sí que es One y es hacer esta transición, pero creo que todas las empresas del mundo están haciendo esta transición poco a poco de software 1.0 a 2.0. ¿Pero cuál es el 2.0? El 2.0 es cuando no tienes código y tienes prompts. Todo tu código de base de código son prompts. Y entonces tú das un servicio a empresas. Especs. Especs, skills, no sé cómo llamarlo, pero contexto.

`01:00:28` **SPEAKER_02** — ¿Y esto lo hace una empresa para ellos mismos?

`01:00:33` **SPEAKER_07** — Esto lo harán las empresas para ellos mismos, será Google, será todas las empresas del mundo. En vez de tener código escrito, estarán prompts, skills, contexto y ficheros.

`01:00:43` **SPEAKER_02** — ¿Pero software para otros o para ellos mismos? O sea, ¿tú estás diciendo que las empresas van a solucionar sus propios problemas haciendo prompts?

`01:00:52` **SPEAKER_07** — Yo lo que digo es que todo el software del mundo cada vez va a ser más prompts y menos código. Vale, bueno, sí. Y eso va a pasar en todos los niveles. ¿Para internamente, externamente?

`01:01:03` **SPEAKER_02** — Estoy de acuerdo. Y ahí es donde el challenge del junior, ¿eh? O sea, el challenge del junior no es tanto en... va a aprender a programar o con agentes de código. Es, va a nacer en un paradigma donde ya no hay código, digamos. O sea, hay prompts y hay muchas capas que para nosotros han sido muy importantes y que hoy se dan por sentadas, ¿sabes? Y alguien que nace ya en este mundo se mueve más rápido en este mundo.

`01:01:27` **SPEAKER_08** — O sea, no lo sé. Sí, para mí el channel de Junior es como de expuesto hasta el problema, desde el principio. Porque el problema ya pasa a ser el foco principal, ¿sabes? Nosotros estamos un poco posicionados con legend to legend. Sí. Por eso también estamos con lo de los pronts y tal, y estamos enamorados de Talas, ¿sabes? ¿Qué es Talas? Estamos esperando. Talas es una empresa que ha metido un LLM dentro de un chip, ¿no? Entonces tenemos 17.000 tokens por segundo de output. Contra los 60, 80 que tenemos ahora, 17.000. 30 y pico de... 30 y pico. ¡Qué barbaridad! Entonces, cuando tengamos 50.000 tokens por segundo, ¿qué hacemos? ¿Sabes? El ordenador es ese chip con un LLM que te genera 50.000 tokens de Go por segundo. Es que es una locura. Y es multimodal y te genera... Te lo hace todo, ¿sabes?

`01:02:18` **SPEAKER_02** — ¿Adrià, tú qué piensas? ¿De? Del debate de los juniors, por ejemplo. O del software hecho con prompts y no con código. Para empezar, es mucho más caro.

`01:02:32` **SPEAKER_01** — O sea, tener software con prompts es mucho más caro. Yo creo que el valor del AI es que te permite expandir el mercado del software, porque hasta ahora el software era algo muy determinista, que se hacía para cubrir muchas casuísticas a la vez, y ahora el AI lo que te permite es hacer cosas que no son tan deterministas. Al final, vas de crud, que es como el primer software que se hizo, bases de datos, formularios, a workers en el mundo real que atacan al mercado, al TAM de los salarios y de las horas humanas, y no al TAM de software para administrar esta economía.

`01:03:12` **SPEAKER_02** — Yo te hago challenge de que sea más caro, ¿eh? Porque, o sea, depende cuándo se ejecuta el prompt. Si el prompt se ejecuta, cada ejecución, cada instancia es carísimo. Si los prompts se ejecutan cada vez que se cambia la configuración, entonces no es tan caro, ¿no? Depende cuándo esté pensado ejecutar los prompts, ¿no?

`01:03:31` **SPEAKER_01** — Ya, pero si, al final todo el software son solo prompts, cada vez que lo usas lo ejecutas y es... muchos órdenes de magnitud más caro.

`01:03:38` **SPEAKER_02** — No, no, no, no, porque puedes configurarlo con prompts.

`01:03:41` **SPEAKER_01** — Yo creo que luego se genera un

`01:03:43` **SPEAKER_02** — workflow, eventualmente se genera... O sea, Claude lo que hace, Claude escribe código para responder.

`01:03:48` **SPEAKER_01** — Sí, sí, yo creo que la magia está en tener un software determinista, que es código que se ejecuta, y encima poner la capa del LLM que transforma este software, la adapta, y también te permite hacer más casuísticas más complejas, que no son deterministas, que tienen ya lógica, que podría sustituir el trabajo diario de un humano.

`01:04:09` **SPEAKER_09** — Yo creo que eso ya lo estamos haciendo a día de hoy, pero no lo vemos como una realidad. Se os pregunta a cada uno de vosotros. Que hay dos aproximaciones, que el ELEM te lo haga constantemente o que tú hayas generado un código que después reutilices, ¿no? Pero yo os cuento mi caso y seguro que vosotros tenéis lo mismo. ¿Cuántos de vosotros estáis utilizando cualquiera de los programas de servicio? ¿Que hace un año ibais a la web a ver los dashboards que te generaban? versus utilizar ese mismo servicio como una fuente de datos y construirte tú automáticamente usando el EMP tu dashboard personalizado con la visualización que tú quieres. Sin las restricciones de ese producto, ¿no? O sea, algo típico que uso todos los días es el Atlassian y los tickets. O sea, yo ya no voy cero a Atlassian a revisar nada. He construido mi propia web con mi propia visualización, con mis propias reglas, solo utilizo Atlassian como fuente de datos.

`01:05:05` **SPEAKER_03** — ¿Y tú crees que eso lo va a hacer cualquiera en el futuro? ¿O crees que lo haces tú porque ya podías hacerlo antes?

`01:05:10` **SPEAKER_09** — Yo creo que a día de hoy es más accesible a mí porque todavía requiere unos fundamentos, pero creo que en la oficina lo está haciendo muchísima gente que no son ingenieros. En la oficina, pero

`01:05:22` **SPEAKER_03** — ¿en una peluquería, por ejemplo?

`01:05:24` **SPEAKER_09** — Pues en la peluquería, por ejemplo, el otro día me crucé con un chico allí en la calle que es camionero, un vecino, y le habían hecho una prueba médica Y entonces me estaba explicando cómo él, con Chachipití, que es un usanantrópico, cómo él se había hecho su propio diagnóstico, había hecho... y al final ha sacado un informe que era más acurate que el que le había dado el especialista. Ahora no lo sabe. Bueno, sí, porque lo confrontó con el especialista. O sea, cuando fue al especialista fue con su informe previo. Y el especialista le

`01:06:03` **SPEAKER_02** — dijo, ¿de dónde has sacado esto?

`01:06:04` **SPEAKER_09** — Efectivamente. Y yo le digo, Chachipití, ahora me está jodiendo el negocio a mí también. ¿A cuánto estamos de que ellos realmente... le puedes decir ya con voz, como habéis dicho, cuál es la visualización que tú quieres que lo construya al vuelo?

`01:06:16` **SPEAKER_05** — Pero también no significa solo código, porque vemos ahora más un poco noticias de esta semana, que casi todo proveedor ahora tiene un computer use. o si es perplexity, o si es antropic, si es no sé qué. Por eso no hace falta a veces escribir código. Tú dices que mira, vas a Jira y encuentras todo lo que hay. Ya está. Va a clicar, va a hacer esto y no hace falta.

`01:06:39` **SPEAKER_03** — Sí, pero luego también hay empresas que el internet lleva 30 años inventado y siguen guardando todo en papel, siguen guardando todo en tickets. Y estamos en 2026, ¿no? Entonces estamos diciendo, en dos años, todas estas empresas que siguen guardando todo en papel, ¿Van a pasar a usar agentes, a confiar en un agente, a usar tooling online o va a ser una transición más larga?

`01:07:00` **SPEAKER_09** — ¿Serán competitivas en dos años? ¿Versus los que las usen?

`01:07:04` **SPEAKER_02** — El timing es lo más jodido de saber, pero es lo más importante. Porque todos sabemos que en el largo plazo hay AGI. La pregunta es, ¿qué va a pasar mañana?

`01:07:14` **SPEAKER_05** — ¿Cómo somos nosotros los primeros? Dice que la próxima versión de GPT, whatever, va a cambiar. Es AGI. Casi. No, casi. No, no, no. Dice otra. Hay otra palabra. Que dice ahora que va a cambiar en manera sustentativa economía del mundo. No dice AGI, pero dice que es tan grande.

`01:07:34` **SPEAKER_02** — Es lo que tiene estar en permanente fanraising, tío. Hay que estar diciendo muchas cosas. Oye, Edu, déjame el micro un momento, que voy a preguntar a Farrán. ¿Podemos girar aquí la cámara? No sé por qué he escondido aquí a Farrán. Farrán, una pregunta. Tú llevas en Factorial, eres el empleado más antiguo de Factorial. Actualmente, ¿vale? Es el empleado más pionero de Factorial. Tú has visto centenares de desarrolladores pasar por Factorial. Entonces, en este debate de cuál es el perfil que funciona en Factorio, junior, senior, staff, mid, no sé qué, ¿qué ves tú? ¿Qué piensas ahí?

`01:08:14` **SPEAKER_04** — Te he visto antes

`01:08:14` **SPEAKER_02** — hacer caras, por eso digo, te voy a pasar el micro.

`01:08:16` **SPEAKER_04** — Para mí la... La característica principal para una persona que rinde es la motivación. Ves juniors motivados, ves staffs motivados y son los que hacen el click, son los que marcan la diferencia en el desarrollo. También para mí es la gente que se preocupa del producto. Es decir, ves gente que shipea mucho código constantemente, pero lo que decíamos antes de mergeo y me voy. No es mergeo y me voy, es mergeo, me preocupo de cómo ha ido el deploy, los resultados, hay errores de Sentry. Es decir, esa preocupación Y no solo en los deploys, sino en la salud del producto, cómo evoluciona la arquitectura y todos estos factores que determinan cómo tu producto puede escalar durante años.

`01:09:23` **SPEAKER_02** — ¿Crees que la arquitectura de Factorial, tú llevas DX, que es Developer Experience. ¿Qué es Developer Experience? ¿Puedes explicarlo para la gente? Por favor, por favor, que la gente lo entenderá. Y de paso me sirve a mí.

`01:09:40` **SPEAKER_04** — Hacemos de todo menos DX, pero bueno.

`01:09:42` **SPEAKER_05** — Ahora eso ya experience, ¿no?

`01:09:45` **SPEAKER_04** — Exacto. En teoría nuestro equipo se preocupa de que el resto de desarrolladores tengan las herramientas óptimas para el desarrollo, ¿no? Es decir, editores, tooling y demás. Pero aparte hacemos muchísimas más cosas, como por ejemplo mantenimiento del CI, todo el cluster de Kubernetes que tenemos que rinda y podamos testear, revisar los pull requests cada día y mantenerlo a flote porque a veces Por ejemplo, en estas últimas semanas hemos recibido mucha tralla y mantener los tiempos en unos valores razonables es challenging. Y a veces lo ignoramos. Todo el mundo quiere shippear el código rápido, pero la carga que eso implica en el CI y tal es todo un reto.

`01:10:42` **SPEAKER_02** — Farran, ¿tú crees que se va a poder automatizar tirar código?

`01:10:50` **SPEAKER_04** — Yo creo que va a ser una evolución en el tiempo. A corto plazo, los ingenieros vamos a ser más reticentes y tal. Vamos a apostar por esos agentes que te pueden hacer el 90% y nos dejen el 10% o ese 10% sea contexto que no tiene la IA y experiencia que no tiene la IA y nosotros podamos revisar esos pull requests. a medio plazo, largo plazo, va a ser insostenible. Es decir, vamos a tener que mergear confiando ya con lo que dedica la gente. ¿Y la similitud que has dicho antes tú del Assembler? ¿Del Assembler? Yo creo que es una comparación muy válida. Me imagino los ingenieros cuando transicionaron de asemblea a código. Los primeros meses, los primeros años, no, es que no me fío de que escriban las instrucciones los punteros. Pues nos está pasando exactamente lo mismo. Y en cualquier revolución industrial los que venían del paso anterior, pues tienen sus reticencias. Pero cuando ves que la cosa funciona, funciona, funciona, funciona, y el 99% de las veces funciona, te tienes que apostar.

`01:12:22` **SPEAKER_02** — Vale. Oye, me gustaría tocar algunos temas más antes de irnos. Futuro del open source.

`01:12:32` **SPEAKER_06** — Miguel. Ojaco. Hostia, tú.

`01:12:33` **SPEAKER_02** — O sea, por decir nombres, ¿eh?

`01:12:35` **SPEAKER_07** — El futuro del open source, yo creo que sigue teniendo futuro. Es decir, cada vez es más barato hacer código. Incluso la misma técnica se puede aplicar para hacer prompts, que eso es un poco distinto de la revolución del assembler al siguiente lenguaje, ¿no? Que es que estas LLMs también son buenas haciendo prompts. Entonces, esa es un poco la diferencia. Entonces, el futuro del open source es que haya mucho más, creo.

`01:13:04` **SPEAKER_08** — Como estrategia de venta es brutal, cada vez hay más y a lo loco. Y todo lo pones open source primero, validas mercado rápido, se hace como súper viral porque todo el mundo tiene acceso. La gente usa Agents y de repente los Agents hacen web search, se miran Twitter, de repente esto se pega, van, vienen al repositorio y estás usando algo que tu agente ha decidido. que usas porque es la leche y es la leche en Twitter y es Open Source. Entonces, en el momento en el que ya es lo suficientemente la leche, le pones un paywall, ¿sabes qué es lo que están haciendo? Tienes Pencil que ahora es gratis, a ver cuánto tiempo es gratis. ¿Qué es Pencil? Pencil es para diseñar con agentes, saca cursores y empieza a tirar componentes en pantalla con varios cursores y te hace el diseño del app y es Open Source. Figma, Open Source. Figma, Open Source, sí.

`01:13:48` **SPEAKER_02** — Pero al ser tan fácil escribir código, ¿no tiene más sentido trabajar en los agentes, en las capabilities de los agentes, y que los agentes creen las librerías, las soluciones que necesites, en lugar de ir a una librería cada vez más grande de soluciones open source? Qué buena suerte encontrando lo que tú buscas.

`01:14:04` **SPEAKER_08** — Sí, esto es un poco lo que tenemos con los misión control. Todo el mundo está construyendo su misión control y por ahora son todos open source. Pero cuando hay tanto, ¿es útil? ¿El qué es útil?

`01:14:15` **SPEAKER_02** — librerías que hace gente, cuando puedes hacer una a un coste muy bajo.

`01:14:20` **SPEAKER_08** — O sea, es útil en el sentido de que tú no has tenido que pensar en eso porque estabas pensando en tantas otras cosas, porque estabas en paralelo que de repente dices, ah, bueno, ¿cuánto me cuesta probar que ese flow es mejor que el que yo tengo? Pues nada, ¿no? Cojo, me abro una terminal en paralelo, le digo a mi agente, publicate esto y prueba, bro, ¿sabes? Tengo este problema, a ver si lo resuelves. Y tienes ese problema y un día lo resuelves y dices, tú, Change y me muevo a otra cosa. Entonces, sí, es útil, pero la competencia es una locura porque todo el mundo está construyendo lo mismo todos los días.

`01:14:48` **SPEAKER_02** — Pero cuando hay tanta competencia desaparecen los mercados hasta cierto punto, ¿no? Cuando se atomiza tanto, tú dirías es que no con la cabeza.

`01:14:56` **SPEAKER_01** — A ver, yo creo que el AI cambia muchas cosas, pero el open source tampoco lo cambia tanto. El open source tiene mucho sentido, el mismo que ha tenido siempre, y el sentido que tiene el open source son las economías de escala y los network effects, porque al hacer tecnología abierta, el resto de la tecnología se construye ahí encima.

`01:15:19` **SPEAKER_02** — Ya, pero la gracia era tener un pool de desarrolladores que es todo el mundo, ¿no?

`01:15:24` **SPEAKER_01** — Bueno, es una de las gracias.

`01:15:26` **SPEAKER_02** — Bueno, es la gracia que luego, como derivado, se convirtió en canal de distribución.

`01:15:29` **SPEAKER_01** — Pero, por ejemplo, esto se transforma en tener que los agentes, el training set, por ejemplo, imagínate, Factorial está escrito en React, ¿no? Imagínate que en vez de coger React de Facebook, hacemos nuestro framework JavaScript de reactividad. Pues los LLMs, como React es el estándar, están entrenados para saber ya React, saber cómo se escribe la sintaxi. Si lo hubiésemos hecho in-house, esta ventaja no la tendríamos. Y por lo tanto, el open source tiene mucho sentido ahí.

`01:16:03` **SPEAKER_02** — Eso es hasta hoy. Pero la pregunta es a partir de hoy. O sea, ¿cómo se van a producir estas concentraciones marginales de soluciones?

`01:16:12` **SPEAKER_05** — Me parece que es open source para mí. Porque al final yo no veo open source como código. Yo veo open source como ideas, ideas, implementaciones y un poco esos mad scientists compartiendo con todo el mundo sus aficiones, sus ambiciones. Y ahora, artefacto cambia. Que no exponemos código, exponemos skills, exponemos software 2.0, no sé qué. Pero al final la idea sirve y continúa. Es verdad que toda governance que tenemos por ahí, tenemos que repensar. Porque yo veo que GitHub está cayendo ahora porque hay tanto overload. Y ya escribiendo un montón de pull request issues. Y todo el mundo con repositorios muy populares está cerrando todo porque es imposible revisar. un código que está generando la IA. Esto tenemos que revisar, pero la idea continúa. Yo, personalmente, estoy robando a veces tantos skills de personas que me gustan porque tienen ideas muy potentes. Y es como, uy, sí, es verdad. Yo voy a coger esto, voy a coger esto. Para mí eso es open source. Tienes que hacer hiding también. Yo tengo todos mis skills abiertos. Y no sé si alguien está leyendo o revisando, pero cada vez que yo estoy encontrando algo, yo lo estoy poniendo en open source.

`01:17:27` **SPEAKER_02** — Vale. Autoresearch, quería preguntaros. ¿Alguien ha utilizado Autoresearch?

`01:17:33` **SPEAKER_00** — Hostia, ahora me dejáis como no sé qué. O sea, sí, yo he estado trasteando un poquito con Autoresearch.

`01:17:39` **SPEAKER_02** — Autoresearch es un repositorio que ha publicado Carpacci, ¿no? Sí, correcto. Como que ha inventado la piedra filosofal. Igual no es tan piedra filosofal, pero…

`01:17:48` **SPEAKER_00** — El concepto es muy bueno, ¿no? O sea, yo corro un programa, un LLM en mi repositorio, o en lo que quiera realmente, pero generalmente en un repositorio, le doy varios experimentos que puede hacer y lo dejo corriendo ahí durante X ciclos, ¿no? Y entonces al final, si yo le doy unos benchmarks claros, va a correr estos experimentos en secuencia y entonces me va a sacar el output, ¿no? Entonces la idea es, oye, lo dejas corriendo dos o tres días, ¿no? O no sé cuántos ciclos de experimentos, o una noche y te levantas por la mañana, y te encuentras que te ha tirado, no sé, seis cómics en una branch que te dice, oye, he aumentado la performance de este proceso de factorial en un 16%.

`01:18:26` **SPEAKER_02** — Pero es una tarea como mejorar la performance de este proceso. Lo que tú le digas. No le puedes decir

`01:18:30` **SPEAKER_00** — lo que he dicho antes, Julio. Traeme 50 millones de euros de RR. A ver, en teoría sí, ¿no? No sé si lo vamos a ver hacer súper bien. ¿Cuántos días tardará? No sé para qué está optimizado, pero sí, el concepto me parece muy interesante.

`01:18:42` **SPEAKER_02** — Bueno, no está optimizado para nada, simplemente va experimentando todo lo que hay en el mundo, ¿no?

`01:18:46` **SPEAKER_00** — Pero feedback loop es muy largo.

`01:18:49` **SPEAKER_02** — El feedback loop es lo que tú quieres que sea, lo puedes configurar, ¿no?

`01:18:52` **SPEAKER_05** — No, pero ¿cómo tú vas a medir MRR con el feedback loop? Necesitas esperar un poco.

`01:18:59` **SPEAKER_08** — Igual consigue, pero igual tarda más que nosotros. Sí, eso es.

`01:19:04` **SPEAKER_00** — Chao, Miguel. Sí, entonces lo que yo he estado intentando pensar es, vale, ahora yo lo puedo correr en mi ordenador, ¿cómo lo corremos en común en Factorial y lo ponemos en común, no? Para que el compute, digamos, o sea, para que todos los ordenadores, imagínate, yo qué sé, los 300 personas y pico de producto que estamos en Factorial, menos los tres que estén haciendo sus experimentos, podamos correr varios experimentos en paralelo durante toda la noche, por la mañana, pues no tengamos los cinco que he corrido yo, sino tengamos pues 1.500 experimentos que nos mejoran la performance en cada domain y varias pull requests que... para revisar. Si los benchmarks están claros y esto es capaz de hacerlo, es brutal. Tenemos los ordenadores trabajando para nosotros por la noche en común, además intentando resolver los mismos problemas de performance o de lo que sea. Hay mil cosas que podríamos hacer desde, yo que sé, Por ejemplo, ver si un curso del LMS tiene la estructura adecuada. Hay mil cosas que podríamos hacer aquí con la auto-research que son interesantes.

`01:20:16` **SPEAKER_02** — Vale. Oye, Edu, te devuelvo el micro. He visto que has publicado en LinkedIn un orquestador. ¿Por qué has hecho un orquestador? ¿Qué hace?

`01:20:29` **SPEAKER_03** — Básicamente corre agentes y lo que quería es entender cómo funcionan los agentes. Este 5%, cuando yo le doy una tarea y sale mal, Yo quiero que salga bien y quiero tener control sobre las decisiones que va tomando la gente. Se decía Oriol antes, yo no reviso el código en GitHub porque el feedback loop es demasiado largo. porque tengo que revisar el código. Yo quiero no tener que revisar el código. Si yo, mientras va tomando decisiones, veo las decisiones que los agentes van tomando, no necesito que termine de generar el código para saber que va a generar algo bien o va a generar algo mal. Entonces, la idea de este orquestador es que me vaya diciendo todo el tiempo su proceso mental y yo poder ir guiándolo en esto. Pero bueno, es un experimento sobre todo para aprender dónde están los límites. La idea inicial era, con un agente muy tonto quiero poder llegar a hacer lo que hace un agente más listo. y aprendí que no es posible porque hay un baseline, un mínimo que necesitas. Un agente muy tonto no hace tool calls con un ratio suficiente como para que cuando los corres durante un loop muy largo, va componiendo el error y acaban cosas que no te puedes fiar. Entonces, el mínimo ahora mismo es estos modelos nuevos, el 4.6 y el 5.4, que puedes correr durante mucho tiempo y se van autocorrigiendo cuando cometen errores en vez de irse estropeando cada vez más rápido.

`01:21:51` **SPEAKER_02** — Vale. Y última pregunta para Miguel. Atención al micro, ¿no? Vale. Te iba a preguntar, Miguel, cuando está cambiando todo tanto, cada equipo te viene con, hostia, he probado la última, no sé qué. ¿Cómo decidimos en Factorial de, mira, esto se va a convertir en estándar a partir de ahora? A partir de ahora todo el mundo va a ir subiendo la barra, ¿no? Esto se va a convertir en el mínimo. ¿Cuándo? tomamos o tomas esta decisión de decir, esto, todos los equipos, ahora, venga, managers, directores, a conseguir esto ahora.

`01:22:32` **SPEAKER_09** — O sea, primero es que es una decisión conjunta, la tomamos. Siempre hay alguien que empieza punta de lanza, ¿no? O hacen de ruptor. Generalmente, Xiliar. Después tenemos ahí a Jacob y, bueno, un conjunto de personas que van ahí pues haciendo auto-research. Y dentro de todo eso...

`01:22:52` **SPEAKER_02** — Autoresearch o research sin auto.

`01:22:55` **SPEAKER_09** — Y dentro de todo eso, uno, tenemos que mantener la calma, porque hay personas que avanzan muy rápido, pero después estandarizar eso no es tan sencillo, porque yo, por ejemplo, veo a Ilia, pero Ilia muchas de las cosas que hace son instinto. Tira por aquí, por allá, o hasta qué rápido hemos ido, y claro, cuando queremos estandarizar, tenemos que frenar un poco, ahí entre el equipo de Dx...

`01:23:17` **SPEAKER_02** — Eso es lo que quería aquí, destilar tu skill, Que también tienes que acabar poniéndonos Markdown. ¿Cuál es el momento o cuál es el signo que tú ves de decir, vale, esto, esto sí, estás testeado, ¿por qué ahora sí y por qué no?

`01:23:32` **SPEAKER_09** — La verdad es que solo puedo explicarlo con ejemplos porque yo creo que siempre he tenido esa capacidad de ver el camino, de ver el camino claro de cuáles son los pasos que tenemos que seguir. No soy tan bueno haciendo ese research, que Illian eso es un crack, un fenómeno, pero sí veo las señales de hacia dónde tenemos que ir. Se hizo un trabajo mucho de research el año pasado. Al principio de este año hicimos ese cambio cultural radical que trajimos al equipo, lo hemos contado varias veces. Le pusimos el objetivo de un día una serie de iniciativas que llevaban meses y cero código. Nuestros mejores equipos lo hicieron en esa tarde. Ahí no estandarizamos nada. Simplemente pusimos unas guías para que la gente empezara a experimentar. Eso abrió la mente y la gente empezó a experimentar. Y durante las siguientes dos semanas, ahí encontramos el camino de, oye, ¿cuáles son los puntos? Porque hay siempre diferentes vectores de ataque, ¿no? Cada equipo tiene uno en particular. Encontramos este punto común, ¿no? Donde convergía todo el mundo. Y ese fue el momento en el que pudimos empezar a estandarizar. Y ahí es cuando llegó el equipo de Diex, ¿no? Ahí vino Ferran y David y Olek, todo este equipo que tenemos que es maravilloso. Tres semanas después vinieron con un RFC y unas guidance para todo el equipo de ingeniería, que es el que acabamos de implantar. Y ahí incluimos ya las métricas de uso, etc. Un poco ese es el camino que seguimos. Y después también es... Esto es iterativo. También hay feedback en esto, ¿no? Vamos aprendiendo y vamos cambiando cosas. Y vamos aprendiendo cosas en paralelo. Ahora estamos trabajando en las specs, ¿no? ¿Cómo estandarizamos las specs? Eso a partir también de que estas semanas todo el mundo tiene su concepto de spec. que en cada equipo es distinto. Y también Illya ha ido haciendo un research de cuál es su visión. Entonces, de la visión de Illya, que siempre es muy avanzada, lo que hacen los equipos, encontraremos otra vez el punto medio donde nos ponemos otra vez de acuerdo. Dx está trabajando también en ese punto común y así avanzamos.

`01:25:38` **SPEAKER_02** — Pero una cosa que sí que es brutal es, realmente ha habido una transformación como nunca he visto en los últimos meses en el equipo de Factorial. Hemos cambiado la forma de generar soluciones a problemas y de trabajar conjuntamente. Creo que hay un momentum súper interesante y algo está pasando que muchas empresas nos están pidiendo que que les hagamos workshops de cómo hemos hecho el cambio y cómo estamos construyendo el producto a día de hoy. Aunque realmente es algo que cambia, como hemos visto en esa discusión, sigue cambiando, ¿no? Exactamente.

`01:26:11` **SPEAKER_09** — Y hay personas, o sea, yo creo que próximos días o la semana que viene compartiremos un poco estos workshops con algunas empresas que han venido también a compartirnos el punto en el que están ellos, cómo están avanzando los challenges, explicarles cómo nosotros estamos resolviendo también desde la realidad, ¿no? Pero todavía veo esa resistencia en el resto del mundo. Yo, así, tampoco es que sea muy comedido o tal, pero quiero decir, yo veo que hay una línea que está ahí liderando globalmente, de tres, que son Anthropic, OpenAI y, bueno, no sé si Google o Congeminate o tal, ¿no? Después hay una línea por detrás de ellos, creo que ahí estamos nosotros, honestamente. Y después vienen otro grupo de empresas, ¿no? Hay todavía mucha reticencia. La gente todavía busca el modelo anterior de la estandarización, del determinismo, de este mundo enterprise. Entonces, en estas charlas que tenemos, el 90% de la conversación es cómo hacemos todo determinista, ¿no? En lugar de... Cargar trails a todo. Exacto. Cómo nos movemos a este nuevo... Bueno, y ahí estamos compartiendo

`01:27:20` **SPEAKER_02** — Es que no es obvio, ¿eh? O sea, el tema de pasar a confiar en otro agente externo a ti, externo a la empresa, que va a tomar las decisiones más críticas. Con Human on the Loop, sin Human on the Loop, es igual. Pero decisiones críticas por nosotros, pues como ingenieros, es un poco antiintuitivo.

`01:27:42` **SPEAKER_09** — Hay un poco de acto de C, esa carrera que tiene que hacer.

`01:27:47` **SPEAKER_02** — Uriel, ¿quieres dar alguna última novedad de One? Antes de cerrar algún highlight? algún breakthrough?

`01:28:00` **SPEAKER_05** — ¿Quieres? Sí. No, me parece es como… Es que ahora no has pilado aquí yo contra mí. No estaba pensando en eso. Dejando las perdas, ¿no?

`01:28:07` **SPEAKER_02** — Lo tienes que aprobar. ¿Ves? El vender.

`01:28:11` **SPEAKER_05** — No, no es verdad. Esta semana hemos salido tantos funciones en la One porque todos los equipos están metiendo toda la información de Factorial y brutal cómo crece esto. Pero para mí, el momento que flipé yo fue cuando he visto Que One ahora genera dashboards de todo analítica, para mí, en el momento de pregunta, yo quiero. Exactamente para mí, que estamos hablando de antes que UI va a ser algo generativo para exactamente un caso de uso que yo tengo. Ahora es la realidad en One en factorial. Tú puedes preguntar, ¿qué quieres a nivel de datos? Y si es algo que está mejor representado en gráficos, mejor que texto, One va a generar un dashboard solo para ti en este momento.

`01:28:52` **SPEAKER_02** — Esto, hablando de ceder el control o aceptar el indeterminismo en tu vida, nunca me había pasado en la vida que voy a ver un cliente. Ayer fui a ver un cliente en Madrid. y tal, y claro, dicen, bueno, quiero probar mi prompt, ¿no? Y yo digo, ¿seguro que no quieres el mío? No, no, vamos a probar qué quieres, ¿no? Y cuando tú ves que te pide lo más remoto que se te ocurra y de golpe Juan le pinta un dashboard exactamente como si le hiera el cerebro con todo lo que está pidiendo, con el gráfico, con la evolución, con las métricas principales, la gente flipa. Yo primero. Yo soy el primero que digo, ¿en serio? Nunca me había pasado de hacer una demo y yo ser el que más flipa mientras voy haciendo la demo. O sea que esto... brutal. Muy bien. Pues nada, chicos. Muchísimas gracias. ¿Alguien se ha dejado algo por decir? ¿No? Pues gracias a todos y con los demás. Hasta la semana que viene.
