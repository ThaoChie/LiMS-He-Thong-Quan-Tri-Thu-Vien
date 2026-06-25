from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import BookProposal
from .forms import ProposalCreateForm


@login_required
def proposal_list_view(request):
    proposals = BookProposal.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(proposals, 10)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'proposals/proposal_list.html', {'page_obj': page})


@login_required
def proposal_create_view(request):
    if request.method == 'POST':
        form = ProposalCreateForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.user = request.user
            proposal.save()
            messages.success(request, 'Đề xuất đã được gửi thành công!')
            return redirect('proposals:proposal_list')
    else:
        form = ProposalCreateForm()
    return render(request, 'proposals/proposal_create.html', {'form': form})


@login_required
def proposal_detail_view(request, pk):
    proposal = get_object_or_404(BookProposal, pk=pk)
    if proposal.user != request.user and request.user.role not in ['librarian', 'admin']:
        messages.error(request, 'Không có quyền xem.')
        return redirect('home')
    return render(request, 'proposals/proposal_detail.html', {'proposal': proposal})


@login_required
def review_proposals_view(request):
    if request.user.role not in ['librarian', 'admin']:
        messages.error(request, 'Không có quyền.')
        return redirect('home')
    status_filter = request.GET.get('status', '')
    proposals = BookProposal.objects.all().select_related('user')
    if status_filter:
        proposals = proposals.filter(status=status_filter)
    paginator = Paginator(proposals.order_by('-created_at'), 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'proposals/review_proposals.html', {'page_obj': page, 'status_filter': status_filter})


@login_required
def review_proposal_action_view(request, pk):
    if request.user.role not in ['librarian', 'admin']:
        messages.error(request, 'Không có quyền.')
        return redirect('home')
    proposal = get_object_or_404(BookProposal, pk=pk, status='pending')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ['approved', 'rejected']:
            proposal.status = action
            proposal.admin_notes = request.POST.get('admin_notes', '')
            proposal.reviewed_by = request.user
            proposal.save()
            label = 'phê duyệt' if action == 'approved' else 'từ chối'
            messages.success(request, f'Đã {label} đề xuất "{proposal.title}".')
    return redirect('proposals:review_proposals')
