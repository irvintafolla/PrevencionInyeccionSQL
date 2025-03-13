import re

def obtener_recomendacion(codigo, extension):
    """Detecta vulnerabilidad y devuelve una recomendación con código corregido"""
    recomendaciones = []


    if extension == ".py":
         #  SQL Injection
        if re.search(r"execute\(\s*f?['\"].*\{.*\}['\"]\s*\)", codigo, re.IGNORECASE):
            recomendaciones.append({
                "mensaje": "Se detectó posible SQL Injection en Python. Usa sentencias preparadas con parámetros.",
                "explicacion": "Las sentencias preparadas son una forma segura de ejecutar consultas SQL en Python. Al usar sentencias preparadas, los valores de los parámetros se pasan por separado, evitando la inyección de SQL. ",
                "ejemplo_corregido": '''import sqlite3
                    conn = sqlite3.connect("db.sqlite")
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))'''
            })

        #  OS Command Injection
        if re.search(r"os\.system\(\s*f?['\"].*['\"]\s*\)", codigo):
            recomendaciones.append({
                "mensaje": "Se detectó uso inseguro de `os.system()`. Valida entradas antes de ejecutar comandos.",
                "explicacion": "Los comandos en Python deben ser validados para evitar inyección de comandos. Usar `subprocess.run()` es una buena alternativa.",
                "ejemplo_corregido": '''import subprocess
                    comandos_permitidos = ["ls", "whoami"]
                    if comando in comandos_permitidos:
                        subprocess.run([comando])'''
          })

        #  XSS en Python con Flask
        if re.search(r"return\s*f?['\"].*<.*>.*['\"]", codigo):
            recomendaciones.append({
                "mensaje": "Se detectó posible XSS en Flask. Usa `html.escape()` para sanitizar la salida.",
                "explicacion": "La función `html.escape()` escapa los caracteres especiales en HTML, evitando ataques XSS.",
                "ejemplo_corregido": '''from flask import Flask, request
                    import html

                    app = Flask(__name__)
                    @app.route("/comentarios")
                    def comentarios():
                        comentario = html.escape(request.args.get("comentario"))
                        return f"<h1>{comentario}</h1>"'''
            })

        # Hardocoded credenciales
        if re.search(r"=[\s]*['\"](?!https?:\/\/).*['\"]", codigo):
            recomendaciones.append({
                "mensaje": "Se detectaron credenciales en el código. Usa variables de entorno en su lugar.",
                "explicacion": "Las credenciales en el código son un riesgo de seguridad. Usa variables de entorno para almacenar credenciales de forma segura.",
                "ejemplo_corregido": '''import os 
                    API_KEY = os.getenv("API_KEY")'''
            })

        if re.search(r"eval\(\s*['\"].*['\"]\s*\)", codigo):
            recomendaciones.append({
                "mensaje": "Se detectó uso inseguro de `eval()`. Valida entradas antes de ejecutar comandos.",
                "explicacion": "La función `eval()` ejecuta código Python arbitrario, lo que puede ser peligroso. Evita su uso en aplicaciones en producción.",
                "ejemplo_corregido": '''import subprocess
                    comandos_permitidos = ["ls", "whoami"]
                    if comando in comandos_permitidos:
                        subprocess.run([comando])'''
            })


        if re.search(r"pickle\.loads\(\s*.*\s*\)",codigo):
            recomendaciones.append({
                "mensaje": "Se detectó uso de `pickle.loads()`. Evita deserializar datos no confiables.",
                "explicacion": "La función `pickle.loads()` deserializa datos no confiables, lo que puede ser peligroso. Evita su uso en aplicaciones en producción.",
                "ejemplo_corregido": '''# Usa alternativas seguras como `json` o `yaml`
                    import json
                    data = json.loads(serialized_data)'''
            })

        # 🔍 Weak Password Storage (Use bcrypt or Argon2 instead)
        if re.search(r"hashlib\.md5\(|hashlib\.sha1\(", codigo):
            recomendaciones.append({
                "mensaje": "Se detectó almacenamiento inseguro de contraseñas. Usa bcrypt o Argon2 en su lugar.",
                "explicacion": "No almacenes contraseñas con algoritmos débiles como MD5 o SHA1. Usa funciones de hashing seguras como bcrypt o Argon2.",
                "ejemplo_corregido": '''import bcrypt
                password = b"mi_contraseña_segura"
                hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                if bcrypt.checkpw(password, hashed):
                    print("Contraseña válida")'''
                        })

        # 🔍 Missing Multi-Factor Authentication (MFA)
        if re.search(r"def login\(", codigo):
            recomendaciones.append({
                "mensaje": "El sistema de autenticación no parece incluir autenticación de dos factores (2FA).",
                "explicacion": "MFA reduce el riesgo de accesos no autorizados. Implementa 2FA con códigos temporales o notificaciones push.",
                "ejemplo_corregido": '''import pyotp

                secret = pyotp.random_base32()
                totp = pyotp.TOTP(secret)
                print("Código MFA:", totp.now())  # Comparar con la entrada del usuario'''
            })

        # 🔍 Insecure Encryption (Use AES Instead)
        if re.search(r"Crypto\.Cipher\.DES|Crypto\.Cipher\.ARC4", codigo):
            recomendaciones.append({
                "mensaje": "Se detectó uso de cifrado inseguro (DES/RC4). Usa AES con una clave segura.",
                "explicacion": "DES y RC4 son obsoletos y vulnerables a ataques. Usa AES con un modo seguro como GCM.",
                "ejemplo_corregido": '''from Crypto.Cipher import AES
                import os

                key = os.urandom(32)  # 256-bit secure key
                cipher = AES.new(key, AES.MODE_GCM)
                ciphertext, tag = cipher.encrypt_and_digest(b"mensaje secreto")'''
            })

        # 🔍 JWT Validation (Prevent Token Manipulation)
        if re.search(r"jwt\.decode\(", codigo):
            recomendaciones.append({
                "mensaje": "Se detectó uso de JWTs. Asegúrate de validarlos correctamente con una clave segura.",
                "explicacion": "Los JWTs pueden ser manipulados si la clave secreta es débil. Usa una clave segura y verifica la firma.",
                "ejemplo_corregido": '''import jwt

                SECRET_KEY = "clave_super_secreta"
                token = jwt.encode({"usuario": "admin"}, SECRET_KEY, algorithm="HS256")

                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                    print("Token válido:", payload)
                except jwt.ExpiredSignatureError:
                    print("Token expirado")
                except jwt.InvalidTokenError:
                    print("Token inválido")'''
            })

        # 🔍 API Rate Limiting (Prevent DoS Attacks)
        if re.search(r"from flask import Flask", codigo):
            recomendaciones.append({
                "mensaje": "No se detectó limitación de peticiones en la API. Implementa rate limiting.",
                "explicacion": "Las APIs sin limitación de solicitudes pueden ser vulnerables a ataques de denegación de servicio (DoS). Usa `Flask-Limiter` para restringir el tráfico.",
                "ejemplo_corregido": '''from flask import Flask
                from flask_limiter import Limiter

                app = Flask(__name__)
                limiter = Limiter(app, key_func=lambda: "global")

                @app.route("/")
                @limiter.limit("10 per minute")
                def index():
                    return "Hola, mundo"'''
            })


        #  Código  seguro por defecto si no se detectó nada específico
        if not recomendaciones:
            recomendaciones.append({
                "mensaje": "Código vulnerable, pero no se identificó la falla específica. Revisa las prácticas de seguridad.",
                "explicacion": "",
                "recomendacion": "Revisa la documentación de seguridad de tu lenguaje para mejorar tu código."
            })

    elif extension == ".cs" :
        #  SQL Injection
        if re.search(r"(SELECT|INSERT|DELETE|UPDATE)\s+\*\s*FROM\s+[a-zA-Z_]+.*['\"].*['\"]", codigo, re.IGNORECASE):
            recomendaciones.append({
                "mensaje": "Se detectó posible SQL Injection. Usa sentencias preparadas con `SqlParameter`.",
                "explicacion": "Las sentencias preparadas son una forma segura de ejecutar consultas SQL en C#. Al usar sentencias preparadas, los valores de los parámetros se pasan por separado, evitando la inyección de SQL.",
                "ejemplo_corregido": """using System.Data.SqlClient;
                    SqlCommand cmd = new SqlCommand("SELECT * FROM usuarios WHERE nombre = @usuario", conexion);
                    cmd.Parameters.AddWithValue("@usuario", usuario);"""
            })

        #  OS Command Injection
        if re.search(r"Process\.Start\(\s*['\"].*['\"]\s*\)", codigo):
            recomendaciones.append({
                "mensaje": "Se detectó uso inseguro de `Process.Start()`. Valida entradas antes de ejecutar comandos.",
                "explicacion": "Los comandos en C# deben ser validados para evitar inyección de comandos. Usa `ProcessStartInfo` para ejecutar comandos de forma segura.",
                "ejemplo_corregido": """using System.Diagnostics;
                    if (comando == "dir" || comando == "ipconfig") {
                    Process.Start(new ProcessStartInfo("cmd.exe", "/C " + comando) { RedirectStandardOutput = true });
                    }"""
            })

        #  XSS (Cross-Site Scripting)
        if re.search(r"Response\.Write\(|Console\.WriteLine\(|document\.write\(", codigo):
            recomendaciones.append({
                "mensaje": "Se detectó posible XSS. Usa `HttpUtility.HtmlEncode()` para sanitizar la salida.",
                "explicacion": "La función `HttpUtility.HtmlEncode()` escapa los caracteres especiales en HTML, evitando ataques XSS.",
                "ejemplo_corregido": """using System.Web;
                    string inputSeguro = HttpUtility.HtmlEncode(inputUsuario);
                    Response.Write(inputSeguro);"""
            })

        #  Hardcoded credenciales
        if re.search(r"(User\s*Id\s*=\s*['\"].*['\"]|Password\s*=\s*['\"].*['\"])", codigo, re.IGNORECASE):
            recomendaciones.append({
                "mensaje": "Se detectaron credenciales en el código. Usa variables de entorno en su lugar.",
                "explicacion": "Las credenciales en el código son un riesgo de seguridad. Usa variables de entorno para almacenar credenciales de forma segura.",
                "ejemplo_corregido": """using Microsoft.Extensions.Configuration;
                    var config = new ConfigurationBuilder().AddJsonFile("appsettings.json").Build();
                    string dbPassword = config["Database:Password"];"""
            })

        
        # Acceso a archivos inseguro
        if re.search(r"File\.ReadAllText\(\s*['\"].*['\"]\s*\)", codigo):
            recomendaciones.append({
                "mensaje": "Se detectó acceso inseguro a archivos. Usa rutas seguras y verifica permisos.",
                "explicacion": "El acceso directo a archivos sin validar puede exponer información sensible o permitir acceso a archivos no autorizados. Asegúrate de validar rutas y permisos antes de abrir archivos.",
                "ejemplo_corregido": """using System.IO;

                    string rutaSegura = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments), "archivo.txt");
                    string contenido = File.ReadAllText(rutaSegura);"""
            })


        #  Weak Password Storage
        if re.search(r"PasswordDeriveBytes|SHA1\.Create\(\)", codigo):
            recomendaciones.append({
                "mensaje": "Se detectó almacenamiento inseguro de contraseñas. Usa bcrypt o PBKDF2 en su lugar.",
                "explicacion": "No almacenes contraseñas con algoritmos débiles como SHA1 o MD5. Usa funciones de derivación de claves como bcrypt o PBKDF2.",
                "ejemplo_corregido": """using System.Security.Cryptography;
                    using BCrypt.Net;

                    string hashedPassword = BCrypt.Net.BCrypt.HashPassword(password);
                    bool isValid = BCrypt.Net.BCrypt.Verify(passwordIngresada, hashedPassword);"""
            })

        #  Missing Multi-Factor Authentication (MFA)
        if re.search(r"Login\(\s*.*\s*\)", codigo):
            recomendaciones.append({
                "mensaje": "El sistema de autenticación no parece incluir autenticación de dos factores (2FA).",
                "explicacion": "MFA reduce el riesgo de accesos no autorizados. Implementa 2FA usando códigos temporales o notificaciones push.",
                "ejemplo_corregido": """using Google.Authenticator;

                    TwoFactorAuthenticator tfa = new TwoFactorAuthenticator();
                    var setupInfo = tfa.GenerateSetupCode("MiAplicacion", usuario.Email, secretKey, false, 3);
                    string qrCodeUrl = setupInfo.QrCodeSetupImageUrl;
                    // Muestra el código QR al usuario para que lo escanee en su app de autenticación"""
            })

        #  Insecure Encryption (Use AES Instead)
        if re.search(r"DES\.Create\(\)|RC4\.Create\(\)", codigo):
            recomendaciones.append({
                "mensaje": "Se detectó uso de cifrado inseguro (DES/RC4). Usa AES con una clave segura.",
                "explicacion": "DES y RC4 son obsoletos y vulnerables a ataques. Usa AES con un modo seguro como GCM.",
                "ejemplo_corregido": """using System.Security.Cryptography;

                    Aes aes = Aes.Create();
                    aes.Key = Convert.FromBase64String("clave-segura");
                    aes.GenerateIV();
                    // Usa AES en modo GCM o CBC con padding seguro"""
            })

        #  JWT Validation (Prevent Token Manipulation)
        if re.search(r"new JwtSecurityToken\(", codigo):
            recomendaciones.append({
                "mensaje": "Se detectó generación de JWTs. Asegúrate de validarlos correctamente con una clave segura.",
                "explicacion": "Los JWTs pueden ser manipulados si la clave secreta es débil. Usa claves seguras y verifica la firma.",
                "ejemplo_corregido": """using System.IdentityModel.Tokens.Jwt;
                    using Microsoft.IdentityModel.Tokens;

                    var tokenHandler = new JwtSecurityTokenHandler();
                    var key = Encoding.ASCII.GetBytes("clave-super-secreta");

                    tokenHandler.ValidateToken(token, new TokenValidationParameters
                    {
                        ValidateIssuerSigningKey = true,
                        IssuerSigningKey = new SymmetricSecurityKey(key),
                        ValidateIssuer = false,
                        ValidateAudience = false
                    }, out SecurityToken validatedToken);"""
            })

        #  API Rate Limiting (Prevent DoS Attacks)
        if re.search(r"app\.UseRouting\(\)", codigo):
            recomendaciones.append({
                "mensaje": "No se detectó limitación de peticiones en la API. Implementa rate limiting.",
                "explicacion": "Las APIs sin limitación de solicitudes pueden ser vulnerables a ataques de denegación de servicio (DoS). Usa `IThrottleStore` o `AspNetCoreRateLimit` para limitar el tráfico.",
                "ejemplo_corregido": """using AspNetCoreRateLimit;
                    
                    services.Configure<IpRateLimitOptions>(options =>
                    {
                        options.GeneralRules = new List<RateLimitRule>
                        {
                            new RateLimitRule
                            {
                                Endpoint = "*",
                                Period = "1s",
                                Limit = 10
                            }
                        };
                    });"""
            })

        #  Código  seguro por defecto si no se detectó nada específico
        if not recomendaciones:
            recomendaciones.append({
                "mensaje": "Código vulnerable, pero no se identificó la falla específica. Revisa las prácticas de seguridad.",
                "explicacion": "",
                "recomendacion": "Revisa la documentación de seguridad de tu lenguaje para mejorar tu código."
            })

    return recomendaciones