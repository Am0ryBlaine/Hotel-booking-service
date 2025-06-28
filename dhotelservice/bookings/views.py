from django.http import HttpResponse, JsonResponse
import json
from .models import Room
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import Hotel


def index(request):
    return HttpResponse('Страница приложения бронирования номеров отелей')


@csrf_exempt
def add_room(request):
    if request.method != 'POST':
        return HttpResponse ({'Ошибка': 'Метод не разрешен'}, status=405)
    try:
        data = json.loads(request.body)
        description = data.get('description')
        price = data.get('price_per_night')
        hotel_id = data.get('hotel_id')

        if description is None or price is None or hotel_id is None:
            return JsonResponse({'Ошибка': 'Отсутствует описание,цена за ночь или hotel_id'}, status=400)

        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            return JsonResponse({'Ошибка': 'Отель с таким id не найден'}, status=404)

        room = Room.objects.create(description=description, price_per_night=price,hotel=hotel)
        return JsonResponse({'id': room.id})
    except Exception as e:
        return JsonResponse({'Ошибка': str(e)}, status=400)


@csrf_exempt
def delete_room(request):
    if request.method != 'DELETE':
        return JsonResponse({'Ошибка': 'Метод не разрешен'}, status=405)
    try:
        data = json.loads(request.body)
        room_id = data.get('id')
        if room_id is None:
            return JsonResponse({'Ошибка': 'Не найден номер'}, status=400)
        deleted_count, _ = Room.objects.filter(id=room_id).delete()
        if deleted_count == 0:
            return JsonResponse({'Ошибка': 'Комната не найдена'}, status=404)
        return JsonResponse({'Статус': 'удалён'})
    except Exception as e:
        return JsonResponse({'Ошибка': str(e)}, status=400)


def list_rooms(request):
    sort_param = request.GET.get('sort','date_asc')
    order_by_field={
        'price_asc': 'price_per_night',
        'price_desc': '-price_per_night',
        'date_asc': 'created_at',
        'date_desc': '-created_at'
    }.get(sort_param,'created_at')

    rooms = Room.objects.all().order_by(order_by_field)

    result=[]
    for room in rooms:
        result.append({
            'Номер': room.id,
            'Описание': room.description,
            'Цена за ночь': str(room.price_per_night),
            'Дата создания': room.created_at.isoformat()
        })

    return JsonResponse(result, safe=False)


@csrf_exempt
def add_booking(request):
    if request.method != 'POST':
        return JsonResponse({'Ошибка': 'Метот не разрешен'}, status=405)
    try:
        data = json.loads(request.body)
        room_id = data.get('room_id')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')

        if None in (room_id, start_date_str, end_date_str):
            return JsonResponse({'Ошибка': 'Отсутствует параметры'}, status=400)

        # Парсим даты
        try:
            start_date = datetime.strptime(start_date_str,'%d.%m.%Y').date()
            end_date = datetime.strptime(end_date_str,'%d.%m.%Y').date()
        except ValueError:
            return JsonResponse({'Ошибка': 'Некорректный формат даты'}, status=400)

        if start_date > end_date:
            return JsonResponse({'Ошибка': 'Дата начала позже даты окончания'}, status=400)

        #Проверка существования комнаты
        from .models import Room, Booking
        room = Room.objects.filter(id=room_id).first()
        if room is None:
            return JsonResponse({'Ошибка': 'Комната не найдена'}, status=404)

        # Создаем бронь
        booking = Booking.objects.create(
            room=room,
            start_date=start_date,
            end_date=end_date
        )
        return JsonResponse({'id': booking.id})
    except Exception as e:
        return JsonResponse({'Ошибка': str(e)}, status=400)



@csrf_exempt
def delete_booking(request):
    if request.method != 'DELETE':
        return JsonResponse({'Ошибка': 'Метод не разрешен'}, status=405)
    try:
        data = json.loads(request.body)
        booking_id = data.get('booking_id')
        if booking_id is None:
            return JsonResponse({'Ошибка': 'Отсутствует ID брони'}, status=400)

        from .models import Booking
        deleted_count, _ = Booking.objects.filter(id=booking_id).delete()
        if deleted_count == 0:
            return JsonResponse({'Ошибка': 'Бронь не найдена'}, status=404)

        return JsonResponse({'Статус': 'удалена'})
    except Exception as e:
        return JsonResponse({'Статус': str(e)}, status=400)


@csrf_exempt
def list_bookings_by_hotel(request):
    try:
        from .models import Booking, Room
        bookings = Booking.objects.all().order_by('start_date')

        result=[]
        for b in bookings:
            result.append({
                'ID брони': b.id,
                'Дата начала': b.start_date.isoformat(),
                'Дата окончания': b.end_date.isoformat()
            })

        return JsonResponse(result, safe=False)
    except Exception as e:
        return JsonResponse({'Ошибка': str(e)}, status=400)