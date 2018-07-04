# -*- coding: utf-8 -*-

import base64
import os
import threading
import uuid
import json
from io import BytesIO
import requests


# DJANGO
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.utils.datetime_safe import datetime
from django.views.generic.base import View

# REST FRAMEWORK
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# SERIALIZERS
from .serializerUserPropietario import PropietarioUserSerializer
from .serializerIntermediate import CompareIntermediateSerializer
from .serializerCompare import CompareSerializer
from .serializerMarca import MarcaSerializer
from .serializerPropietario import PropietarioSerializer
from .models import PropietarioGanado, ImagenMarcaGanado, ComparacionModel, ComparacionItermediate, UsuarioPropietario

# LIBRERIAS GRAFICAS
import numpy as np
import cv2
from skimage.measure import compare_ssim as ssim
import urllib.request

# PDF
from reportlab.pdfgen import canvas


def verifyssl(request):
    file = open(os.path.join(os.path.dirname(__file__),
                             ".well-known/acme-challenge/mUYH46lnjWEzIIMsV5NwBURpJ_3ifY2SPHS3x0AnzC4"))
    return HttpResponse(file, content_type="text/html; charset=utf-8")


def async_compare(img_orig, token):
    try:
        image_rec = _grab_image(stream=img_orig)
        image_rec_rz = cv2.resize(image_rec, (512, 512))
        # image_rec_rz_gray = cv2.imdecode(image_rec_rz, cv2.IMREAD_GRAYSCALE)
        marcas = ImagenMarcaGanado.objects.filter()
        # images_intermediate = ComparacionItermediate.objects.get(id=id)
        list_results = []
        list_complete = []
        for item in marcas:
            with urllib.request.urlopen(item.imagen_comparacion.url) as url:
                s = url.read()

            image = np.asarray(bytearray(s), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
            result = compareImages(image, image_rec_rz)

            data = {
                'documento': item.propietario.documento,
                'nombre': '%s %s %s ' % (
                    item.propietario.nombre, item.propietario.apellido, item.propietario.segundo_apellido),
                'imagen': item.imagen.url,
                'result': result
            }

            # print(data)

            list_complete.append(data)

            if result > 0.7:
                list_results.append(data)

        '''
        images_intermediate.imagen_compare_intermediate = item
        images_intermediate.result_comparation = result
        images_intermediate.save()
                
        images_intermediate.finish_process = True
        images_intermediate.save()
        '''

        print('proceso finalizado')

        if len(list_results) > 0:
            leads_as_json = json.dumps(list_results)
        else:
            leads_as_json = json.dumps(list_complete)

        send_notification(token, leads_as_json, True)

    except Exception as e:
        print(e)
        send_notification(token, {}, False)


def send_notification(token, data, estado):
    url_fcm = 'https://fcm.googleapis.com/fcm/send'
    header = {
        'Authorization': 'key='+'AAAA8VybPkM:APA91bGaRExOheCc17Qz5Pw6sskiqxz6Y8zXPP5JlG8WM7miTXnoi9iKwYg4f1Dt8KjDQgasTY5zgk6vG5dkVjThaKc6h5fuPkL5X4U_8bDHdllCYd6r3NawrhDZXjI8gTfV1dFfGDov',
        'Content-Type': 'application/json'
    }
    payload = {
        'to': token,
        'notification': {
            'title': 'Resultados',
            'body': 'El proceso de comparación ha terminado',
        },
        'data': {
            'resultados': data
        }
    }
    request = requests.post(url_fcm, json=payload, headers=header)
    print(request.text)

    '''
    try:
        push_service = FCMNotification(
            api_key=')
        registration_id = token

        if estado:
            message_title = "Resultados"
            message_body = data
        else:
            message_title = "Error"
            message_body = ""

        push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                          message_body=message_body)
    except Exception as e:
        print(str(e))
    '''


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        usr = request.data.get('username')
        psw = request.data.get('password')

        propietario = UsuarioPropietario.objects.filter(usuario__username=usr)
        if len(propietario) == 0:
            list_response = [{'token': 'jrtrf-sddsd-fgffg', 'tipo': '0'}]
        else:
            list_response = [{'token': 'jrtrf-sddsd-fgffg', 'tipo': '1'}]

        user = authenticate(username=usr, password=psw)

        if user is not None:
            response = {
                'isOk': True,
                'message': '',
                'content': list_response
            }
        else:
            response = {
                'isOk': False,
                'message': 'Usuario inválido, por favor verifique sus credenciales',
                'content': []
            }
        return Response(response, status=status.HTTP_201_CREATED)


class PropietarioView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, doc=None, format=None):
        # token_data = jwt_decode_handler(content)
        # print(token_data)
        if doc is None:
            lista_propietarios = PropietarioGanado.objects.filter(activo=True)
            propietario_serializer = PropietarioSerializer(lista_propietarios, many=True)
            response = {
                'isOk': True,
                'message': '',
                'content': propietario_serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            propietario = PropietarioGanado.objects.filter(documento=doc)
            propietario_serializer = PropietarioSerializer(propietario, many=True)
            response = {
                'isOk': True,
                'message': '',
                'content': propietario_serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

    def post(self, request, format=None):
        doc = request.data.get('documento')
        try:
            PropietarioGanado.objects.get(documento=doc)
            response = {
                'isOk': False,
                'message': 'El documento, ya se encuentra registrado. !',
                'content': []
            }
        except:
            serializer = PropietarioSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'isOk': True,
                    'message': 'Datos guardados correctamente. !',
                    'content': []
                }
            else:
                response = {
                    'isOk': False,
                    'message': serializer.errors,
                    'content': []
                }
        return Response(response, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, format=None):
        try:
            propietario = PropietarioGanado.objects.get(documento=pk)
            propietario.activo = False
            propietario.save()
            response = {
                'isOk': True,
                'message': 'Propietario eliminado correctamente',
                'content': []
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except PropietarioGanado.DoesNotExist:
            response = {
                'isOk': False,
                'message': 'Propietario no encontrado',
                'content': []
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                'isOk': False,
                'message': str(e),
                'content': []
            }
            return Response(response, status=status.HTTP_201_CREATED)


class PropietarioViewUpdate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        id = request.data.get('id')
        documento = request.data.get('documento')
        primer_nombre = request.data.get('nombre')
        segundo_nombre = request.data.get('segundo_nombre')
        primer_apellido = request.data.get('apellido')
        segundo_apellido = request.data.get('segundo_apellido')
        ciudad = request.data.get('ciudad')
        direccion = request.data.get('direccion')
        finca = request.data.get('finca')
        region = request.data.get('departamento')
        telefono = request.data.get('telefono')

        try:
            propietario = PropietarioGanado.objects.get(id=id)
            propietario.documento = documento
            propietario.nombre = primer_nombre
            propietario.segundo_nombre = segundo_nombre
            propietario.apellido = primer_apellido
            propietario.segundo_apellido = segundo_apellido
            propietario.ciudad = ciudad
            propietario.direccion = direccion
            propietario.finca = finca
            propietario.region = region
            propietario.telefono = telefono

            propietario.save()

            lista_propietarios = PropietarioGanado.objects.all()
            propietario_serializer = PropietarioSerializer(lista_propietarios, many=True)

            response = {
                'isOk': True,
                'message': 'Datos actualizados correctamente. !',
                'content': propietario_serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                'isOk': False,
                'message': str(e),
                'content': []
            }
            return Response(response, status=status.HTTP_201_CREATED)


class UsuarioPropietarioView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):

        usuarios = UsuarioPropietario.objects.all()
        serializer_usuarios = PropietarioUserSerializer(usuarios, many=True)
        response = {
            'isOk': True,
            'message': '',
            'content': serializer_usuarios.data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def post(self, request, fotmat=None):

        propietario_id = request.data.get('propietario')
        propietario_usuario = request.data.get('usuario')
        propietario_contrasena = request.data.get('contrasena')

        try:
            usuario = UsuarioPropietario.objects.get(propietario__id=propietario_id)
            if propietario_usuario == 'None':
                usr = User.objects.get(username=usuario.usuario.username)
                usr.set_password(propietario_contrasena)
                usr.save()
                response = {
                    'isOk': True,
                    'message': 'Contraseña cambiada correctamente',
                    'content': []
                }
            else:
                response = {
                    'isOk': False,
                    'message': 'El propietario, ya pose un usuario asignado',
                    'content': []
                }
            return Response(response, status=status.HTTP_201_CREATED)
        except UsuarioPropietario.DoesNotExist:
            propietario = PropietarioGanado.objects.get(id=propietario_id)
            user = User.objects.create_user(propietario_usuario, propietario_contrasena)
            user.save()
            propietario_user = UsuarioPropietario.objects.create(
                propietario=propietario, usuario=user)
            propietario_user.save()
            response = {
                'isOk': True,
                'message': 'Usuario creado satisfatoriamente',
                'content': []
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                'isOk': False,
                'message': str(e),
                'content': []
            }
            return Response(response, status=status.HTTP_201_CREATED)


class UploadImageMarcaView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, documento=None, format=None):
        if documento is not None:
            try:
                marcaGanadero = ImagenMarcaGanado.objects.filter(propietario__documento=documento)
                marcaGanaderoSerializer = MarcaSerializer(marcaGanadero, many=True)
                response = {
                    'isOk': True,
                    'message': '',
                    'content': marcaGanaderoSerializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            except Exception as e:
                response = {
                    'isOk': False,
                    'message': e,
                    'content': []
                }
                return Response(response, status=status.HTTP_201_CREATED)

    def post(self, request, format=None):
        documento = request.data.get('documento')
        img = request.FILES['image']
        tipo = request.data.get('type')
        print(documento)
        try:
            propietario = PropietarioGanado.objects.get(documento=documento)
            if tipo == '0':
                imagenMarca = ImagenMarcaGanado.objects.create(propietario=propietario, imagen=img)
                imagenMarca.save()
            else:
                imagenMarca = ImagenMarcaGanado.objects.get(propietario=propietario)
                imagenMarca.imagen_comparacion = img
                imagenMarca.save()

            response = {
                'isOk': True,
                'message': 'Marca cargada correctamente',
                'content': []
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                'isOk': False,
                'message': 'Ha ocurrido un error, marca no encontrada',
                'content': []
            }
            return Response(response, status=status.HTTP_201_CREATED)


class UploadImageMarcaCompareView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        registration_id = request.data.get('registration_id')
        if request.FILES.get("image", None) is not None:
            image_origin = request.FILES["image"]
            hilo = threading.Thread(target=async_compare, args=(image_origin, registration_id))
            hilo.start()
            response = {
                'isOk': True,
                'message': 'Imagen cargada correctamente, recibiras una notificación con los resultado resulados',
                'content': [],
                # 'id': marcas_intermediate.id
            }
        else:
            response = {
                'isOk': False,
                'message': 'Error al cargar la imagen intente nuevamente',
                'content': []
            }
            '''
            # marcas_intermediate = ComparacionItermediate.objects.create()
            # marcas_intermediate.save()
            '''
        return Response(response, status=status.HTTP_201_CREATED)


class SaveImageCompare(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        id_marca = request.data.get('id_marca')
        image = request.data.get('image')
        porcentaje_coincidencia = request.data.get('coincidencia')

        try:
            # marca = ImagenMarcaGanado.objects.get(propietario__id=id_marca)
            marca = ImagenMarcaGanado.objects.get(propietario__documento=id_marca)
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4())[:12] + '.' + ext)

            marca_compare = ComparacionModel()
            marca_compare.imagen_marca = marca
            marca_compare.imagen_muestra = data
            marca_compare.fechaDeSubida = datetime.now()
            marca_compare.result_comparation = porcentaje_coincidencia
            marca_compare.save()

            response = {
                'isOk': True,
                'message': 'Imagen guardada correctamente',
                'content': []
            }
            return Response(response, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            response = {
                'isOk': False,
                'message': 'Ha ocurrido un error, intente nuevamente',
                'content': []
            }
            return Response(response, status=status.HTTP_201_CREATED)


class GetImagesCompare(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        compareImages = ComparacionModel.objects.all()
        serializer_compare = CompareSerializer(compareImages, many=True)
        response = {
            'isOk': True,
            'message': '',
            'content': serializer_compare.data
        }
        return Response(response, status=status.HTTP_201_CREATED)


class GetImagesIntermediate(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id=None, format=None):
        if id is not None:
            intermediate = ComparacionItermediate.objects.filter(id=id)
            if intermediate[0].finish_process:
                if intermediate[0].imagen_compare_intermediate is not None:
                    data = CompareIntermediateSerializer(intermediate, many=True)
                    response = {
                        'isOk': True,
                        'message': '',
                        'content': data.data
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
                else:
                    data = ImagenMarcaGanado.objects.all()
                    list_response = []
                    for item in data:
                        data_com = ComparacionItermediate()
                        data_com.imagen_compare_intermediate = item
                        list_response.append(data_com)

                    serialize_data = CompareIntermediateSerializer(list_response, many=True)
                    response = {
                        'isOk': True,
                        'message': '',
                        'content': serialize_data.data
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = {
                    'isOk': True,
                    'message': 'Proceso no terminado',
                    'content': []
                }
                return Response(response, status=status.HTTP_201_CREATED)


class ReportePersonasPDF(View):

    def get(self, request, *args, **kwargs):
        # Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        # Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        # Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        # Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = 'https://yhymar.webfactional.com/static/img/alcaldia-logo.jpg'
        # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90, preserveAspectRatio=True)
        # Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


def getDepartamentos(request):
    f = os.path.join(os.path.dirname(__file__), 'departamentos/colombia.json')
    json_data = open(f)
    return HttpResponse(json_data)


def compareImages(imageRecibida, imageOriginal):
    s = ssim(imageOriginal, imageRecibida)
    return s


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    #  sum of the squared difference between the two images;
    #  NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    #  return the MSE, the lower the error, the more "similar"
    #  the two images are
    return err


def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        image = cv2.imread(path)

    # otherwise, the image does not reside on disk
    else:
        # if the URL is not None, then download the image
        if url is not None:
            resp = urllib.urlopen(url)
            data = resp.read()

        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            data = stream.read()

        # convert the image to a NumPy array and then read it into
        # OpenCV format
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)

    # return the image
    return image


def generaPdf(request, pk=None):
    pass
    '''
    if pk is not None:
        comparacion = ComparacionModel.objects.get(id=pk)
        template = get_template("pdf-template.html")
        context = {
            'img_comparacion': comparacion.imagen_muestra.url,
            'img_resultado': comparacion.imagen_marca.imagen.url
        }
        html = template.render(context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None
    '''


