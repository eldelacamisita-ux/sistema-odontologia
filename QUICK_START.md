# ⚡ QUICK START - FASES 2 Y 3

## 🎯 Cambios en 3 Líneas

1. ✅ **SIN CORREOS** - Ya no necesitas configurar SMTP/Resend
2. ✅ **HORARIOS** - Gestiona y muestra horarios de doctores en el dashboard
3. ✅ **PAGOS** - Los pacientes suben comprobantes, admins los aprueban

---

## 🚀 Arranque Rápido (Local)

```bash
cd "c:\Users\Cesar\Desktop\agente odontologia"
python run.py
```

Abre: http://localhost:5000  
Login: `admin` / `admin123`

---

## 🎨 Nuevas Pantallas

### 1. Horarios (`/dashboard/horarios`)
- Ver todos los horarios de doctores
- Agregar nuevo horario (solo admin)
- Eliminar horarios

### 2. Pagos (`/citas/comprobantes/pendientes`)
- Ver comprobantes pendientes de aprobación
- Aprobar o rechazar con motivo
- Ver imágenes de comprobantes

### 3. Subir Comprobante (`/citas/subir-comprobante/<id>`)
- Formulario simple: monto + foto
- Solo para citas "realizadas"
- Formatos: PNG, JPG, PDF (hasta 5MB)

---

## 📋 Flujo Básico de Prueba

```
1. Login como admin
   ↓
2. Dashboard → Ver 4 horarios iniciales
   ↓
3. Horarios → Agregar uno nuevo
   ↓
4. Citas → Crear cita de prueba
   ↓
5. Citas → Cambiar estado a "realizada"
   ↓
6. Citas → Click "Subir comprobante"
   ↓
7. Subir imagen (5 o 10 $)
   ↓
8. Pagos → Ver comprobante pendiente
   ↓
9. Aprobar o Rechazar
   ↓
10. Citas → Ver badge de estado (verde/rojo)
```

---

## 🎨 Cambios Visuales

### Menú
```
Antes: Dashboard | Pacientes | Citas | Auditoría | Agentes

Ahora: Dashboard | Pacientes | Citas | 🕐 Horarios | 💵 Pagos | Auditoría | Agentes
```

### Dashboard
```
ANTES:
┌─────────────────┐
│ Estadísticas    │
│ Próximas Citas  │
│ Gráficos        │
└─────────────────┘

AHORA:
┌─────────────────┐
│ Estadísticas    │
│ Próximas Citas  │
│ 🆕 Horarios     │
│ Gráficos        │
│ 🆕 Acciones     │
└─────────────────┘
```

### Listado de Citas
```
ANTES:
Paciente | Fecha | Motivo | Estado | Acciones

AHORA:
Paciente | Fecha | Motivo | Estado + 🆕 Badge Pago | Acciones + 🆕 Subir
```

---

## 🔐 Permisos

| Acción | Admin | Paciente |
|--------|:-----:|:--------:|
| Ver horarios | ✅ | ✅ |
| Gestionar horarios | ✅ | ❌ |
| Subir comprobante | ✅ | ✅* |
| Aprobar/Rechazar | ✅ | ❌ |

*Solo su propia cita

---

## 📁 Archivos Clave

```
app/
├── models.py                      ← +2 modelos
├── templates/
│   ├── horarios/                  ← +2 archivos
│   ├── citas/
│   │   ├── subir_comprobante.html ← +1 archivo
│   │   └── comprobantes_pendientes.html ← +1 archivo
├── static/
│   └── comprobantes/              ← carpeta nueva
```

---

## 🐛 Problemas Comunes

### No veo horarios en dashboard
**Solución:** La BD ya existía. Reinicia:
```bash
rm instance/odontologia.db
python run.py
```

### Error al subir archivo
**Verifica:**
- Tamaño < 5MB
- Formato: PNG, JPG, JPEG, GIF, PDF
- Cita en estado "realizada"

### No puedo acceder a "Pagos"
**Verifica:** Debes estar logueado como **odontólogo**

---

## 📤 Deploy a Render

```bash
# 1. Commit
git add .
git commit -m "feat: Fases 2 y 3 - Horarios y comprobantes"

# 2. Push
git push origin main

# 3. Render despliega automáticamente
# Espera 2-5 minutos
```

---

## 📚 Documentación Completa

- `README_CAMBIOS.md` - Resumen ejecutivo
- `FASES_2_Y_3_COMPLETADAS.md` - Documentación técnica
- `CHECKLIST_FINAL.md` - Lista de verificación
- `DEPLOY_RENDER_FASES_2_3.md` - Guía de deployment

---

## ✅ Checklist Mínimo

- [ ] Aplicación arranca sin errores
- [ ] Veo 4 horarios en dashboard
- [ ] Puedo agregar un horario
- [ ] Puedo subir un comprobante
- [ ] Puedo aprobar/rechazar comprobantes
- [ ] Badges se muestran correctamente

---

## 🎉 ¡Listo!

**Todo funcionando →** Hacer commit y push

**Algo no funciona →** Ver documentación completa

---

**Versión:** 2.0.0  
**Actualizado:** 16/06/2026  
**Estado:** ✅ LISTO
