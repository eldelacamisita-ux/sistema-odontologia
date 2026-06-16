# ✅ CHECKLIST FINAL - FASES 2 Y 3

## 🎯 Verificación de Implementación

### ✅ Archivos Creados

- [x] `app/models.py` - Modelos HorarioDoctor y ComprobantePago agregados
- [x] `app/templates/horarios/listar.html` - Listado de horarios
- [x] `app/templates/horarios/formulario.html` - Formulario de horarios
- [x] `app/templates/citas/subir_comprobante.html` - Subir comprobante
- [x] `app/templates/citas/comprobantes_pendientes.html` - Gestión de pagos
- [x] `app/static/comprobantes/.gitkeep` - Carpeta para archivos
- [x] `FASE1_COMPLETADA.md` - Documentación Fase 1
- [x] `FASES_2_Y_3_COMPLETADAS.md` - Documentación Fases 2 y 3
- [x] `RESUMEN_IMPLEMENTACION.md` - Resumen completo

### ✅ Archivos Modificados

- [x] `app/__init__.py` - Seed de horarios iniciales
- [x] `app/main/routes.py` - Rutas de horarios y horarios en dashboard
- [x] `app/citas/routes.py` - Rutas de comprobantes
- [x] `app/templates/base.html` - Enlaces en menú
- [x] `app/templates/index.html` - Card de horarios
- [x] `app/templates/citas/listar.html` - Indicadores de pago
- [x] `.gitignore` - Ignorar comprobantes de pago

### ✅ Configuración

- [x] `config.py` - UPLOAD_FOLDER y MAX_CONTENT_LENGTH ya configurados
- [x] Carpeta `app/static/comprobantes/` creada
- [x] Seed de datos de horarios implementado

---

## 🧪 Pruebas a Realizar

### Horarios

1. **Visualización**
   - [ ] Los horarios iniciales aparecen en el dashboard
   - [ ] Los horarios se muestran agrupados por doctor
   - [ ] El enlace "Horarios" funciona en el menú

2. **Gestión (como odontólogo)**
   - [ ] Puedo acceder a `/dashboard/horarios`
   - [ ] Puedo agregar un nuevo horario
   - [ ] El horario se guarda correctamente
   - [ ] Puedo eliminar un horario existente
   - [ ] La confirmación de eliminación funciona

3. **Permisos**
   - [ ] Los pacientes pueden ver horarios pero no gestionar
   - [ ] Solo odontólogos ven el botón "Agregar horario"

### Comprobantes de Pago

1. **Visualización**
   - [ ] El enlace "Pagos" aparece solo para odontólogos
   - [ ] Los badges de estado aparecen en el listado de citas

2. **Subir Comprobante (como paciente o admin)**
   - [ ] El botón aparece solo en citas "realizadas"
   - [ ] Puedo seleccionar monto (5 o 10)
   - [ ] Puedo seleccionar archivo (PNG, JPG, PDF)
   - [ ] El archivo se sube correctamente
   - [ ] Aparece mensaje de éxito

3. **Validaciones**
   - [ ] No puedo subir archivo de formato incorrecto
   - [ ] No puedo subir archivo mayor a 5MB
   - [ ] No puedo subir comprobante de cita ajena (como paciente)
   - [ ] Solo puedo subir en citas "realizadas"

4. **Gestión (como odontólogo)**
   - [ ] Puedo ver lista de comprobantes pendientes
   - [ ] Puedo ver la imagen del comprobante (click para ampliar)
   - [ ] Puedo aprobar un comprobante
   - [ ] Puedo rechazar un comprobante con motivo
   - [ ] El estado cambia correctamente en el listado

5. **Estados**
   - [ ] Badge verde para "aprobado"
   - [ ] Badge amarillo para "pendiente"
   - [ ] Badge rojo para "rechazado"
   - [ ] No aparece botón de subir si ya está aprobado
   - [ ] Aparece botón de subir si está rechazado

---

## 🚀 Comandos Útiles

### Iniciar la Aplicación
```bash
cd "c:\Users\Cesar\Desktop\agente odontologia"
python run.py
```

### Verificar Modelos
```bash
python -c "from app import create_app; from app.models import HorarioDoctor, ComprobantePago; app = create_app(); print('✅ Modelos OK')"
```

### Acceder a la Aplicación
- URL: http://localhost:5000
- Usuario admin: `admin`
- Contraseña: `admin123`

### Reiniciar Base de Datos (si necesario)
```bash
# CUIDADO: Esto borrará todos los datos
rm instance/odontologia.db
python run.py
```

---

## 📋 Flujo de Prueba Completo

### Paso 1: Horarios
1. Login como `admin` / `admin123`
2. Ir al Dashboard
3. Verificar que aparecen 4 horarios iniciales:
   - Dr. Nelson Rodriguez: Lunes 12:00-15:00
   - Dr. Nelson Rodriguez: Miércoles 12:00-15:00
   - Dra. Werllith Rangel: Martes 08:00-11:00
   - Dra. Werllith Rangel: Jueves 08:00-11:00
4. Click en "Horarios" en el menú
5. Click en "+ Agregar horario"
6. Completar formulario y guardar
7. Verificar que aparece en la lista
8. Eliminar el horario creado

### Paso 2: Crear Cita de Prueba
1. Ir a "Pacientes" → Crear un paciente de prueba
2. Ir a "Citas" → Crear una cita para ese paciente
3. Cambiar estado de la cita a "realizada" (editar cita)

### Paso 3: Subir Comprobante
1. En el listado de citas, buscar la cita "realizada"
2. Verificar que aparece el botón "Subir comprobante"
3. Click en "Subir comprobante"
4. Seleccionar monto (5 o 10)
5. Subir una imagen o PDF de prueba
6. Verificar mensaje de éxito

### Paso 4: Gestionar Pago
1. Click en "Pagos" en el menú (solo como odontólogo)
2. Verificar que aparece el comprobante pendiente
3. Click en la imagen para ver ampliada
4. Probar "Aprobar" → Verificar badge verde en citas
5. O probar "Rechazar" con motivo → Verificar badge rojo

### Paso 5: Verificar Estados
1. Ir a "Citas"
2. Verificar que el badge correcto aparece
3. Si rechazado, verificar que botón "Subir comprobante" vuelve a aparecer
4. Si aprobado, verificar que no aparece el botón

---

## 🔧 Solución de Problemas

### Error: "No module named 'app.models'"
**Solución:** Reiniciar el servidor

### Error: "relation 'horario_doctor' does not exist"
**Solución:** 
```bash
rm instance/odontologia.db
python run.py
```

### No aparecen los horarios iniciales
**Solución:** La base de datos ya existía. Ejecutar:
```python
from app import create_app, db
from app.models import HorarioDoctor
from datetime import time

app = create_app()
with app.app_context():
    if not HorarioDoctor.query.first():
        horarios = [
            HorarioDoctor(doctor="Dr. Nelson Rodriguez", dia_semana="Lunes", hora_inicio=time(12, 0), hora_fin=time(15, 0)),
            HorarioDoctor(doctor="Dr. Nelson Rodriguez", dia_semana="Miércoles", hora_inicio=time(12, 0), hora_fin=time(15, 0)),
            HorarioDoctor(doctor="Dra. Werllith Rangel", dia_semana="Martes", hora_inicio=time(8, 0), hora_fin=time(11, 0)),
            HorarioDoctor(doctor="Dra. Werllith Rangel", dia_semana="Jueves", hora_inicio=time(8, 0), hora_fin=time(11, 0)),
        ]
        db.session.add_all(horarios)
        db.session.commit()
        print("✅ Horarios creados")
```

### Error al subir archivo
**Verificar:**
- Tamaño menor a 5MB
- Formato permitido (PNG, JPG, JPEG, GIF, PDF)
- Carpeta `app/static/comprobantes/` existe

---

## 📊 Estado Final

| Componente | Estado | Nota |
|------------|--------|------|
| Modelos | ✅ | HorarioDoctor, ComprobantePago |
| Rutas | ✅ | Horarios, Comprobantes |
| Templates | ✅ | 4 nuevos templates |
| Permisos | ✅ | Control por rol |
| Seed | ✅ | Horarios iniciales |
| UI | ✅ | Menú, dashboard, badges |
| Validaciones | ✅ | Archivos, permisos |

---

## 🎉 ¡Todo Listo!

Si todas las pruebas pasan, estás listo para:

1. **Hacer commit a Git**
   ```bash
   git add .
   git commit -m "feat: Agregar horarios de doctores y comprobantes de pago (Fases 2 y 3)"
   git push origin main
   ```

2. **Desplegar a producción**
   - Render detectará los cambios automáticamente
   - Verifica que las tablas nuevas se creen
   - Verifica que el seed de horarios se ejecute

3. **Continuar con PWA** (cuando estés listo)

---

**Última actualización:** 16/06/2026
**Estado:** ✅ LISTO PARA COMMIT Y DEPLOY
