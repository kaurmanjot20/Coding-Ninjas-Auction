from django.shortcuts import render, redirect
from django.db.models import Sum
from Teams.models import Team
from Players.models import Group, Individual, Stat
from django.http import JsonResponse
# Create your views here.



def question_view(request):
    if request.method == 'POST':
        correct_answers = int(request.POST.get('correct_answers'))
        purse_value = int(request.POST.get('purse_value'))
        team_id = int(request.POST.get('team_id'))

        # Update the Team model with correct_answers and purse_value
        team = Team.objects.get(team_id=team_id)
        team.correct_answers = correct_answers
        team.purse_value = purse_value
        team.save()

        return JsonResponse({'message': 'Quiz submitted successfully!'})
    else:
        return render(request, 'index.html')



def group_list(request):
    # Fetch all teams and groups
    teams = Team.objects.all()
    groups = Group.objects.all()

    # Calculate group points for each group
    for group in groups:
        # Sum up the stats of all players in the group
        group_stats = Stat.objects.filter(player__group=group)
        total_points = group_stats.aggregate(
            total_points=Sum('fielding') + Sum('bowling') + Sum('batting')
        )['total_points'] or 0  # Ensure 0 if no stats found
        
        # Update the group points
        group.group_points = total_points
        group.save()
    
    # Fetch existing assignments from session first
    previous_assignment = request.session.get('existing_assignments', [])

    # Check for new group assignments and update purse value accordingly
    existing_assignments = set(group.group_id for group in groups if group.alloted_team_id is not None)

    for group in groups:
        # Check if the group was previously assigned to any team
        if group.group_id in existing_assignments and group.group_id not in previous_assignment:
            team = Team.objects.get(team_id=group.alloted_team_id)
            team.purse_value -= group.group_price
            team.save()

    # Store existing assignments in session
    request.session['existing_assignments'] = list(existing_assignments)

    # Pass the data to the template
    context = {
        'teams': teams,
        'groups': groups,
    }

    return render(request, 'group_list.html', context)



def leaderboard_view(request):
    # Get all teams
    all_teams = Team.objects.all()

    # Filter teams with at least 11 players and at least one wicketkeeper
    qualified_teams = []
    for team in all_teams:
        num_players = Individual.objects.filter(group__alloted_team=team).count()
        num_wicketkeepers = Individual.objects.filter(group__alloted_team=team, stats__wicketkeeper=True).count()
        if num_players >= 11 and num_wicketkeepers >= 1:
            qualified_teams.append(team)

    # Calculate total points for each qualified team and store in a dictionary
    total_points_dict = {}
    for team in qualified_teams:
        total_points = 0
        assigned_groups = Group.objects.filter(alloted_team=team)
        for group in assigned_groups:
            total_points += group.group_points
        total_points_dict[team] = total_points
        # Add the total_points attribute to the team object
        team.total_points = total_points

    # Sort teams by total points scored in descending order
    sorted_teams = sorted(qualified_teams, key=lambda team: team.total_points, reverse=True)

    # Pass the data to the template
    context = {
        'teams': sorted_teams,
    }

    return render(request, 'leaderboard.html', context)



def allot_data(request):
    if request.method == 'POST':
        # Get form data
        group_id = request.POST.get('group_id')
        group_price = float(request.POST.get('group_price'))
        alloted_team_id = request.POST.get('alloted_team_id')

        # Check if Allotted Team ID field is empty
        if not alloted_team_id:
            return JsonResponse({'error': 'Please fill out the Allotted Team ID field.'})

        # Fetch the Team instance based on the ID
        try:
            alloted_team = Team.objects.get(team_id=alloted_team_id)
        except Team.DoesNotExist:
            return JsonResponse({'error': 'Allotted Team with given ID does not exist.'})

        # Check if group price exceeds purse value
        if group_price > alloted_team.purse_value:
            return JsonResponse({'error': 'Insufficient purse value'})

        # Check if the group has already been assigned to a team
        if Group.objects.filter(group_id=group_id, alloted_team_id=alloted_team_id).exists():
            return JsonResponse({'error': 'This group has already been assigned to a team.'})

        # Create or update Group object
        group, created = Group.objects.update_or_create(
            group_id=group_id,
            defaults={'group_price': group_price, 'alloted_team_id': alloted_team_id}
        )

        alloted_team.save()

        return JsonResponse({})  # Empty response for success

    return render(request, 'allot_data.html')