# ⚡ The Force System v2.0

> **Documentación Ejecutiva y Análisis Técnico Estructural**  
> Sistema de gestión optimizado para talleres de motocicletas, desarrollado bajo un entorno local enfocado en la persistencia de datos, control de inventarios y flujos de trabajo asíncronos.

---

## 🛠️ Tecnologías Utilizadas
<div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 25px;">
    <span style="background-color: #21262d; color: #3776AB; padding: 5px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; border: 1px solid #30363d;">Python & FastAPI</span>
    <span style="background-color: #21262d; color: #499848; padding: 5px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; border: 1px solid #30363d;">Uvicorn Server</span>
    <span style="background-color: #21262d; color: #E34F26; padding: 5px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; border: 1px solid #30363d;">HTML5 Semántico</span>
    <span style="background-color: #21262d; color: #1572B6; padding: 5px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; border: 1px solid #30363d;">CSS3 Variables</span>
    <span style="background-color: #21262d; color: #F7DF1E; padding: 5px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; border: 1px solid #30363d;">JavaScript Async</span>
</div>

---

## 📊 Módulos del Sistema y Evidencias Técnicas

<!-- CUADRO 1 -->
<div style="background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 30px;">
    <h3 style="color: #ffffff; margin-top: 0;">1. Pantalla de Carga Animada (Splash Screen)</h3>
    <p style="color: #8b949e;">Muestra el logo de The Force centrado, iluminando la interfaz oscura antes de dar acceso al sistema.</p>
    <img src="evidencias/Logo_force.png" alt="Splash Screen" style="width: 100%; max-width: 850px; border-radius: 6px; border: 1px solid #30363d; margin: 15px 0; display: block;">
    <div style="background-color: rgba(88, 166, 255, 0.05); padding: 15px; border-left: 4px solid #58a6ff; border-radius: 4px;">
        <h4 style="color: #58a6ff; margin: 0 0 8px 0; font-size: 14px; text-transform: uppercase;">Análisis Técnico:</h4>
        <ul style="margin: 0; padding-left: 20px; color: #c9d1d9;">
            <li>Bloquea la pantalla completa mediante capas superpuestas (<code>#050505</code>).</li>
            <li>Aplica transformaciones sutiles de escala (<code>transform: scale()</code>) en sincronía con gradientes radiales interactivos.</li>
            <li>Flujo controlado con un retardador JavaScript asíncrono de 2.5 segundos para evitar redirecciones cíclicas.</li>
        </ul>
    </div>
</div>

<!-- CUADRO 2 -->
<div style="background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 30px;">
    <h3 style="color: #ffffff; margin-top: 0;">2. Panel de Control e Indicadores Centrales (Dashboard)</h3>
    <p style="color: #8b949e;">Interfaz principal de administración que centraliza el estado del taller en tiempo real.</p>
    <img src="evidencias/Dashboard.png" alt="Dashboard" style="width: 100%; max-width: 850px; border-radius: 6px; border: 1px solid #30363d; margin: 15px 0; display: block;">
    <div style="background-color: rgba(242, 204, 96, 0.05); padding: 15px; border-left: 4px solid #f2cc60; border-radius: 4px;">
        <h4 style="color: #f2cc60; margin: 0 0 8px 0; font-size: 14px; text-transform: uppercase;">Análisis Técnico:</h4>
        <ul style="margin: 0; padding-left: 20px; color: #c9d1d9;">
            <li>Valida y muestra en la barra superior el usuario autenticado con privilegios de superusuario (Luis Rosales Abad).</li>
            <li>Renderiza de forma reactiva tres KPIs clave: Órdenes Totales, Vehículos en Taller e Ingresos del Día.</li>
            <li>Ejecuta consultas automáticas de stock; al detectar existencias en 0, genera alertas visuales críticas de inmediato.</li>
        </ul>
    </div>
</div>

<!-- CUADRO 3 -->
<div style="background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 30px;">
    <h3 style="color: #ffffff; margin-top: 0;">3. Módulo de Captura y Registro de Órdenes Técnicas</h3>
    <p style="color: #8b949e;">Formulario optimizado para el ingreso estructurado de nuevos servicios al taller.</p>
    <div style="display: flex; flex-direction: column; gap: 12px; margin: 15px 0;">
        <img src="evidencias/Orden1.png" alt="Registro Parte 1" style="width: 100%; max-width: 850px; border-radius: 6px; border: 1px solid #30363d; display: block;">
        <img src="evidencias/Detalle_final.png" alt="Registro Parte 2" style="width: 100%; max-width: 850px; border-radius: 6px; border: 1px solid #30363d; display: block;">
    </div>
    <div style="background-color: rgba(88, 166, 255, 0.05); padding: 15px; border-left: 4px solid #58a6ff; border-radius: 4px;">
        <h4 style="color: #58a6ff; margin: 0 0 8px 0; font-size: 14px; text-transform: uppercase;">Análisis Técnico:</h4>
        <ul style="margin: 0; padding-left: 20px; color: #c9d1d9;">
            <li>Segmentación estricta en tres fases lógicas: Datos Personales (DNI/Teléfono), Datos de la Unidad (Placa, Marca, Modelo, Color) y Descripción del Trabajo.</li>
            <li>Normaliza los insumos mediante listas desplegables (ej: Asignación del tipo de lubricante Lubripower).</li>
            <li>Al procesar, transforma las entradas en un objeto JSON estructurado enviado vía <code>POST</code> asíncrono al controlador de FastAPI.</li>
        </ul>
    </div>
</div>

<!-- CUADRO 4 -->
<div style="background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 30px;">
    <h3 style="color: #ffffff; margin-top: 0;">4. Bitácora Histórica y Auditoría de Servicios</h3>
    <p style="color: #8b949e;">Panel de control para el seguimiento, actualización y auditoría de órdenes activas y pasadas.</p>
    <img src="evidencias/Historial.png" alt="Historial" style="width: 100%; max-width: 850px; border-radius: 6px; border: 1px solid #30363d; margin: 15px 0; display: block;">
    <div style="background-color: rgba(242, 204, 96, 0.05); padding: 15px; border-left: 4px solid #f2cc60; border-radius: 4px;">
        <h4 style="color: #f2cc60; margin: 0 0 8px 0; font-size: 14px; text-transform: uppercase;">Análisis Técnico:</h4>
        <ul style="margin: 0; padding-left: 20px; color: #c9d1d9;">
            <li>Generación automatizada de llaves primarias únicas basadas en marcas de tiempo (<code>ORD-YYYYMMDD...</code>).</li>
            <li>Aplica estilos condicionales CSS según el estado de la reparación (destacando en brillante las unidades <em>En Proceso</em>).</li>
            <li>Permite llamadas individuales por fila para ejecutar cierres contables rápidos o auditar notas internas de mecánicos.</li>
        </ul>
    </div>
</div>

<!-- CUADRO 5 -->
<div style="background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 30px;">
    <h3 style="color: #ffffff; margin-top: 0;">5. Control de Flota de Vehículos Registrados</h3>
    <p style="color: #8b949e;">Base de datos relacional de las unidades vehiculares que han ingresado al ecosistema del taller.</p>
    <img src="evidencias/Vehiculos.png" alt="Control de Flota" style="width: 100%; max-width: 850px; border-radius: 6px; border: 1px solid #30363d; margin: 15px 0; display: block;">
    <div style="background-color: rgba(86, 211, 100, 0.05); padding: 15px; border-left: 4px solid #56d364; border-radius: 4px;">
        <h4 style="color: #56d364; margin: 0 0 8px 0; font-size: 14px; text-transform: uppercase;">Análisis Técnico:</h4>
        <ul style="margin: 0; padding-left: 20px; color: #c9d1d9;">
            <li>Indexación inteligente utilizando las <strong>Matrículas/Placas</strong> de rodaje como claves de alta prioridad para búsquedas en milisegundos.</li>
            <li>Asocia de forma directa los modelos de alta demanda (Yamaha R15, Honda XR 300) junto a sus kilometrajes exactos para gestionar los ciclos de mantenimiento preventivo.</li>
        </ul>
    </div>
</div>

<!-- CUADRO 6 -->
<div style="background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 30px;">
    <h3 style="color: #ffffff; margin-top: 0;">6. Administración de Almacén e Inventario de Repuestos</h3>
    <p style="color: #8b949e;">Módulo avanzado de control de stock, piezas mecánicas y mutaciones de inventario.</p>
    <img src="evidencias/Inventario.png" alt="Inventario" style="width: 100%; max-width: 850px; border-radius: 6px; border: 1px solid #30363d; margin: 15px 0; display: block;">
    <div style="background-color: rgba(255, 123, 114, 0.05); padding: 15px; border-left: 4px solid #ff7b72; border-radius: 4px;">
        <h4 style="color: #ff7b72; margin: 0 0 8px 0; font-size: 14px; text-transform: uppercase;">Análisis Técnico:</h4>
        <ul style="margin: 0; padding-left: 20px; color: #c9d1d9;">
            <li>Incorpora filtros dinámicos con lógica de búsqueda predictiva en tiempo real sobre el lado del cliente.</li>
            <li>Dispone de accesos rápidos codificados por colores para registrar variaciones de stock (Entradas por compras o Salidas por mermas/servicios).</li>
            <li>Clasifica los componentes por calidades (ej: Originales) mostrando costes públicos formateados en la moneda local.</li>
        </ul>
    </div>
</div>

---

## 🔧 Historial de Solución de Conflictos (Hotfixes)

<div style="margin-bottom: 15px;">
    <span style="background-color: rgba(86, 211, 100, 0.15); color: #56d364; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase;">Solucionado</span>
    <h4 style="color: #ffffff; margin: 4px 0;">Conflicto de Bloqueo de Puerto de Red (Errno 98)</h4>
    <p style="color: #8b949e; margin: 0 0 10px 0; font-size: 14px;">Al arrancar el entorno local con <code>python main.py</code>, el servidor web abortaba debido a que una instancia en segundo plano se encontraba usando el puerto 8000. Se solventó rastreando el socket TCP y eliminando la señal colgada vía terminal con comandos POSIX: <code>fuser -k 8000/tcp</code>.</p>
</div>

<div>
    <span style="background-color: rgba(86, 211, 100, 0.15); color: #56d364; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase;">Solucionado</span>
    <h4 style="color: #ffffff; margin: 4px 0;">Error de Carga y Mapeo de Archivos Multimedia Estáticos</h4>
    <p style="color: #8b949e; margin: 0; font-size: 14px;">Las vistas HTML no lograban resolver las rutas relativas de los logotipos e imágenes. Se solucionó implementando el módulo nativo de FastAPI <code>StaticFiles</code> en el script principal de Python, aislando los activos en el directorio <code>/static</code> y adaptando las llamadas a rutas absolutas.</p>
</div>

---

## 👤 Desarrollador
*   **Líder de Proyecto:** Luis Rosales Abad 
*   **Entorno:** Desarrollo Local
*   **Mes - Año:** Mayo 2026
