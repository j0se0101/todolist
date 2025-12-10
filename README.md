---> Todolist

Una aplicación de lista de tareas construido con Next.js que consume una API FastAPI desplegada en AWS Lambda.

---> Componentes
<div align="center">
  
- Gestión de tareas: Crear, listar, actualizar y eliminar tareas (CRUD completo)
- Usuario personalizado: Configurado para el usuario
<div align="center">
<img width="100%" max-width="800px" alt="image" src="https://github.com/user-attachments/assets/0dc82fc3-9c22-4f9a-b1bf-875be42a641b" />
</div>
- Variables de entorno: Configuración flexible de la URL de la API
<div align="center">
<img width="100%" max-width="800px" alt="image" src="https://github.com/user-attachments/assets/8bffbf1c-0b61-4eaf-8e9a-d9b373dae911" />
</div>
- Despliegue: Compatible con Vercel y AWS S3
</div>


---> Stack tecnológico
<div align="center">
  
 Frontend (todo-site/)
- Framework: Next.js (React)
- Lenguaje: TypeScript
- Package Manager: npm/yarn
- Build: Exportación estática (next export)
 Hosting:
- AWS S3 + CloudFront (via CDK)
- Vercel (alternativa)

Backend (api/)
- Framework: FastAPI (Python)
- Lenguaje: Python 3.9+
- Runtime: AWS Lambda (serverless)
- API Gateway: AWS Lambda Function URLs
- Base de datos: AWS DynamoDB (NoSQL)
Dependencias clave:
- mangum - Adaptador ASGI para Lambda
- pydantic - Validación de datos

Infraestructura como Código (todo-infra/)
- Framework: AWS CDK (Cloud Development Kit)
- Lenguaje: TypeScript
Servicios AWS desplegados:
- Lambda: Función serverless para la API
- DynamoDB: Tabla para almacenar tareas
- S3: Bucket para hosting del frontend
- CloudFront: CDN para distribución del frontend
- Lambda Function URLs: Endpoints HTTP para la API
  
</div>


--->Instalación
<div align="center">

Prerrequesitos
Node.js 14.x o superior
- npm o yarn
- API backend desplegada

Instala las dependencias:
- npm install

Crea un archivo .env.local en la raíz del proyecto:

- NEXT_PUBLIC_API_URL=https://tu-lambda-url.lambda-url.us-west-1.on.aws

- Nota: Obtén la URL de tu API después de desplegar la infraestructura CDK (ver [`../todo-infra/README.md`]

Ejecuta el servidor de desarrollo:

- npm run dev
- Abre [http://localhost:3000](http://localhost:3000) en tu navegador.

Exportación Estática (para S3)

- npm run build

</div>
  
