from django.shortcuts import render, get_object_or_404, redirect
from .models import CourtCase
from .forms import CourtCaseForm, SearchForm, SignUpForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .forms import CustomAuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Sign Up View
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Automatically log the user in after signup
            return redirect('home')  # Redirect to home or another page
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Get the username and password from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log the user in
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect('home')  # Redirect to home or another page
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')  # Redirect to home or another page

# Home View
def home(request):
    """Render the home page."""
    return render(request, 'home.html')

# List all court cases
def case_list(request):
    """List all court cases."""
    cases = CourtCase.objects.all()
    return render(request, 'case_list.html', {'cases': cases})

# Create a new court case
@login_required  # Ensures only authenticated users can create court cases
def case_create(request):
    """Create a new court case."""
    if request.method == 'POST':
        form = CourtCaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Court case created successfully.')
            return redirect('case_list')
    else:
        form = CourtCaseForm()
    return render(request, 'case_form.html', {'form': form})

# View details of a specific court case by CIN
@login_required  # Ensures only authenticated users can view case details
def case_detail(request, CIN):
    """View details of a specific court case."""
    case = get_object_or_404(CourtCase, CIN=CIN)
    return render(request, 'case_detail.html', {'case': case})

# Edit an existing court case by CIN
@login_required  # Ensures only authenticated users can edit court cases
def case_edit(request, CIN):
    """Edit an existing court case."""
    case = get_object_or_404(CourtCase, CIN=CIN)
    if request.method == 'POST':
        form = CourtCaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, 'Court case updated successfully.')
            return redirect('case_detail', CIN=case.CIN)
    else:
        form = CourtCaseForm(instance=case)
    return render(request, 'case_form.html', {'form': form})

# Delete a court case by CIN
@login_required  # Ensures only authenticated users can delete court cases
def case_delete(request, CIN):
    """Delete a court case."""
    case = get_object_or_404(CourtCase, CIN=CIN)
    if request.method == 'POST':
        case.delete()
        messages.success(request, 'Court case deleted successfully.')
        return redirect('case_list')
    return render(request, 'case_confirm_delete.html', {'case': case})

# List Pending Cases
@login_required  # Ensures only authenticated users can view pending cases
def pending_cases(request):
    """List pending court cases."""
    cases = CourtCase.objects.filter(status='Pending').order_by('CIN')
    return render(request, 'pending_cases.html', {'cases': cases})

# Search Cases
@login_required  # Ensures only authenticated users can search for cases
def search_cases(request):
    """Search court cases."""
    form = SearchForm(request.GET or None)
    cases = CourtCase.objects.none()  # Start with an empty queryset

    if form.is_valid():
        query = form.cleaned_data.get('query', '').strip()
        if query:
            cases = CourtCase.objects.filter(
                Q(judgment_summary__icontains=query) |
                Q(crime_type__icontains=query)
            )

    return render(request, 'search_results.html', {'form': form, 'cases': cases})
