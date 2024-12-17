from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from tours.models import Destiny, Accommodation
import razorpay
from schedule.models import Booking, Book_details, Payment
from django.views.decorators.csrf import csrf_exempt


def register(request):
    if request.method == "POST":
        u = request.POST['u']
        p = request.POST['p']
        c = request.POST['c']
        f = request.POST['f']
        l = request.POST['l']
        e = request.POST['e']
        if p == c:
            u = User.objects.create_user(username=u, password=p, first_name=f, last_name=l, email=e)
            u.save()
        else:
            return HttpResponse("Passwords are not same")
        return redirect('schedule:login')
    return render(request, 'register.html')


def user_login(request):
    if request.method == "POST":
        u = request.POST['u']
        p = request.POST['p']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('tours:place')
        else:
            return HttpResponse("Invalid Credentials")
    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('schedule:login')


@login_required
def booking(request):
    if request.method == 'POST':
        check_in = request.POST['k']
        check_out = request.POST['o']
        accommodation_name = request.POST['ac']
        destiny_country = request.POST['d']

        try:
            destiny = Destiny.objects.get(country=destiny_country)
            accommodation = Accommodation.objects.get(name=accommodation_name, destiny=destiny)

            # Create and save booking
            b = Booking.objects.create(
                check_in=check_in,
                check_out=check_out,
                destiny=destiny,
                accommodation=accommodation,
                user=request.user
            )
            b.save()
            return redirect('schedule:dashboard')  # Redirect to a confirmation page or dashboard

        except (Destiny.DoesNotExist, Accommodation.DoesNotExist):
            # Handle error if destiny or accommodation doesn't exist
            return render(request, 'booking.html', {
                'error_message': 'Selected destination or accommodation does not exist.'
            })

    # Fetch all destinies and accommodations to pass to the template
    destinies = Destiny.objects.all()
    accommodations = Accommodation.objects.all()

    return render(request, 'booking.html', {
        'links': destinies,
        'link': accommodations
    })


@login_required
def booking(request):
    if request.method == 'POST':
        check_in = request.POST.get('k')
        check_out = request.POST.get('o')
        accommodation_name = request.POST.get('ac')
        destiny_country = request.POST.get('d')
        number_of_guests = request.POST.get('g')

        try:
            # Retrieve the selected destiny and accommodation
            destiny = Destiny.objects.get(country=destiny_country)
            accommodation = Accommodation.objects.get(name=accommodation_name, destiny=destiny)

            # Check if a booking with the same details already exists for this user
            existing_booking = Booking.objects.filter(
                user=request.user,
                destiny=destiny,
                accommodation=accommodation,
                check_in=check_in,
                check_out=check_out
            ).exists()

            if existing_booking:
                # If duplicate booking found, show an error message
                return render(request, 'booking.html', {
                    'error_message': 'You have already booked this destination and accommodation for the selected dates.',
                    'links': Destiny.objects.all(),
                    'link': Accommodation.objects.all()
                })

            # Create and save the new booking
            Booking.objects.create(
                user=request.user,
                destiny=destiny,
                accommodation=accommodation,
                check_in=check_in,
                check_out=check_out,
                number_of_guests=number_of_guests
            )
            return redirect('schedule:dashboard')  # Redirect to the dashboard

        except (Destiny.DoesNotExist, Accommodation.DoesNotExist):
            # Handle the error if destiny or accommodation does not exist
            return render(request, 'booking.html', {
                'error_message': 'Selected destination or accommodation does not exist.',
                'links': Destiny.objects.all(),
                'link': Accommodation.objects.all()
            })

    # If the request method is GET, fetch all destinies and accommodations for the form
    return render(request, 'booking.html', {
        'links': Destiny.objects.all(),
        'link': Accommodation.objects.all()
    })


@login_required
def dashboard(request):
    # Get all bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user)

    # Initialize total price to 0
    total_price = 0

    # Calculate the total price for all bookings
    for booking in bookings:
        days = (booking.check_out - booking.check_in).days
        if days < 1:
            days = 1  # Minimum of one day

        # Calculate price for this booking: rate * number of days * number of guests
        booking_price = booking.accommodation.price_per_night * days * booking.number_of_guests
        booking.total_price = booking_price  # Update the total price for display

        # Accumulate total price for all bookings
        total_price += booking_price

    # Pass the bookings and total price to the template
    context = {
        'bookings': bookings,
        'total_price': total_price
    }
    return render(request, 'dashboard.html', context)


@login_required
def delete(request, i):
    try:
        # Only delete if the booking belongs to the logged-in user
        booking = Booking.objects.get(id=i, user=request.user)
        booking.delete()
    except:
        pass
    return redirect('schedule:dashboard')


@login_required
def book_confirm(request):
    if request.method == "POST":
        address = request.POST['a']
        phone_no = request.POST['p']
        pin = request.POST['n']

        user = request.user
        bookings = Booking.objects.filter(user=user)
        total_price = 0

        # Calculate total price from user's bookings
        for booking in bookings:
            days = (booking.check_out - booking.check_in).days
            if days < 1:
                days = 1
            total_price += booking.accommodation.price_per_night * days * booking.number_of_guests
            # Ensure this calculation is correct

        print(f"Total price before conversion: {total_price}")  # Debug print

        # Validate total price
        if total_price <= 0:
            return render(request, 'bookconfirm.html', {
                'error_message': 'Invalid order amount. Please check your bookings.'
            })

        total_in_paise = int(total_price * 100)  # Convert to paise for Razorpay

        # Ensure total is at least ₹1 (100 paise)
        if total_in_paise < 100:
            return render(request, 'bookconfirm.html', {
                'error_message': 'Order amount must be at least ₹1.Please add more bookings or review the total''amount'
            })

        # Initialize Razorpay client
        client = razorpay.Client(auth=('rzp_test_zl6krAbsL0hjn4', 's02HnvSpQ6iGdPNpTK0bGGPR'))
        response_payment = client.order.create(dict(amount=total_in_paise, currency="INR"))
        order_id = response_payment['id']
        order_status = response_payment['status']

        if order_status == "created":
            # Create a Payment entry
            payment = Payment.objects.create(
                name=user.username,
                amount=total_price,
                book_id=order_id,  # Set order_id as book_id for consistency
                paid=False
            )
            payment.save()

            # Create a Book_details entry for each booking
            for booking in bookings:
                book_details = Book_details.objects.create(
                    accommodation=booking.accommodation,
                    user=user,
                    address=address,
                    phone_no=phone_no,
                    pin=pin,
                    book_id=order_id,  # Use the same order ID for tracking
                    payment_status="pending"
                )
                book_details.save()

        response_payment['name'] = user.username
        context = {'payment': response_payment}
        return render(request, 'payment.html', context)

    return render(request, 'bookconfirm.html')


@csrf_exempt
def payment_status(request, u):
    user = User.objects.get(username=u)
    if not request.user.is_authenticated:
        login(request, user)

    status = "failed"  # Default status
    if request.method == "POST":
        response = request.POST
        print(response)

        # Ensure response keys match the expected names from Razorpay
        param_dict = {
            'razorpay_order_id': response.get('razorpay_order_id'),
            'razorpay_payment_id': response.get('razorpay_payment_id'),
            'razorpay_signature': response.get('razorpay_signature'),
        }

        client = razorpay.Client(auth=('rzp_test_zl6krAbsL0hjn4', 's02HnvSpQ6iGdPNpTK0bGGPR'))
        print("Client initialized:", client)

        try:
            # Verify the payment signature
            status = client.utility.verify_payment_signature(param_dict)
            print("Payment verification status:", status)

            # Update the payment status in the Payment model
            payment = Payment.objects.get(book_id=response.get('razorpay_order_id'))
            payment.razorpay_payment_id = response.get('razorpay_payment_id')
            payment.paid = True
            payment.save()

            # Update payment status in Book_details
            book_details = Book_details.objects.filter(user=user, book_id=response.get('razorpay_order_id'))
            for detail in book_details:
                detail.payment_status = "paid"
                detail.save()

            # Optionally clear the bookings after successful payment
            bookings = Booking.objects.filter(user=user)
            bookings.delete()

        except razorpay.errors.SignatureVerificationError:
            print("Signature verification failed.")
            status = "failed"

    return render(request, 'pay_status.html', {'status': status})
