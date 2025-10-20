from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from DigiTrackProject.tourism.models import Homestay, Room, Booking, HomestayFeature, CustomUser
from django.db.models import Count
import json


class Command(BaseCommand):
    help = 'Report duplicate Homestay owners and optionally merge duplicate homestays into one (safe, dry-run available).'

    def add_arguments(self, parser):
        parser.add_argument('--list', action='store_true', help='List owners that have more than one homestay')
        parser.add_argument('--owner-id', type=int, help='Owner id to operate on')
        parser.add_argument('--owner-username', type=str, help='Owner username to operate on')
        parser.add_argument('--keep-id', type=int, help='Homestay id to keep')
        parser.add_argument('--delete-ids', type=str, help='Comma-separated homestay ids to delete')
        parser.add_argument('--dry-run', action='store_true', help="Don't perform DB changes, just print actions")
        parser.add_argument('--confirm', action='store_true', help='Confirm destructive actions (must be set to actually delete)')

    def handle(self, *args, **options):
        if options['list']:
            dup_qs = Homestay.objects.values('owner').annotate(c=Count('id')).filter(c__gt=1)
            out = []
            for item in dup_qs:
                owner_id = item['owner']
                owner = CustomUser.objects.filter(id=owner_id).first()
                homestays = list(Homestay.objects.filter(owner_id=owner_id).values('id', 'name', 'address'))
                out.append({'owner_id': owner_id, 'owner_username': owner.username if owner else None, 'count': item['c'], 'homestays': homestays})
            self.stdout.write(json.dumps(out, ensure_ascii=False, indent=2))
            return

        # Identify owner by id or username
        owner = None
        if options.get('owner_id'):
            owner = CustomUser.objects.filter(id=options['owner_id']).first()
        elif options.get('owner_username'):
            owner = CustomUser.objects.filter(username=options['owner_username']).first()

        if not owner:
            raise CommandError('Owner not specified or not found. Use --list to see duplicates, or supply --owner-id/--owner-username')

        homestays = list(Homestay.objects.filter(owner=owner).order_by('id'))
        if len(homestays) <= 1:
            self.stdout.write('Owner has 0 or 1 homestay; nothing to merge.')
            return

        self.stdout.write(f"Found {len(homestays)} homestays for owner {owner.username} (id={owner.id}):")
        for h in homestays:
            self.stdout.write(f"  id={h.id} name={h.name!r} address={h.address!r}")

        # Determine keep and delete ids
        keep_id = options.get('keep_id')
        delete_ids = []
        if options.get('delete_ids'):
            delete_ids = [int(x.strip()) for x in options['delete_ids'].split(',') if x.strip()]

        if keep_id is None:
            # default: keep the first
            keep = homestays[0]
            keep_id = keep.id
            self.stdout.write(f'No --keep-id provided: defaulting to keep id={keep_id}')
        else:
            keep = Homestay.objects.filter(id=keep_id, owner=owner).first()
            if not keep:
                raise CommandError(f'keep-id {keep_id} not found for this owner')

        # If delete_ids not provided, compute them as all except keep
        if not delete_ids:
            delete_ids = [h.id for h in homestays if h.id != keep_id]

        # Verify delete_ids belong to owner and are not the keep id
        delete_ids = [i for i in delete_ids if i != keep_id and any(h.id == i for h in homestays)]

        if not delete_ids:
            self.stdout.write('No homestays selected for deletion after filtering; aborting.')
            return

        # Print planned actions
        self.stdout.write('\nPlanned actions:')
        self.stdout.write(f'  Keep homestay id={keep_id}')
        self.stdout.write(f'  Delete homestay ids={delete_ids}')

        # Show counts of related objects that would be moved
        total_rooms = Room.objects.filter(homestay_id__in=delete_ids).count()
        total_bookings = Booking.objects.filter(homestay_id__in=delete_ids).count()
        total_features = HomestayFeature.objects.filter(homestay_id__in=delete_ids).count()
        self.stdout.write(f'  Rooms to reassign: {total_rooms}')
        self.stdout.write(f'  Bookings to reassign: {total_bookings}')
        self.stdout.write(f'  Features to reassign: {total_features}')

        if options['dry_run']:
            self.stdout.write('\nDry-run mode: no changes performed. Add --confirm to execute.')
            return

        if not options['confirm']:
            raise CommandError('Destructive action requires --confirm. Add --confirm to actually perform the merge.')

        # Perform the merge in a transaction
        with transaction.atomic():
            keep_obj = Homestay.objects.select_for_update().get(id=keep_id)
            # Reassign Rooms
            rooms_moved = Room.objects.filter(homestay_id__in=delete_ids).update(homestay=keep_obj)
            # Reassign Bookings
            bookings_moved = Booking.objects.filter(homestay_id__in=delete_ids).update(homestay=keep_obj)
            # Reassign Features
            features_moved = HomestayFeature.objects.filter(homestay_id__in=delete_ids).update(homestay=keep_obj)
            # Delete duplicate homestays
            deleted_count, _ = Homestay.objects.filter(id__in=delete_ids).delete()

        self.stdout.write('\nMerge complete:')
        self.stdout.write(f'  Rooms moved: {rooms_moved}')
        self.stdout.write(f'  Bookings moved: {bookings_moved}')
        self.stdout.write(f'  Features moved: {features_moved}')
        self.stdout.write(f'  Homestay rows deleted (including cascades): {deleted_count}')
