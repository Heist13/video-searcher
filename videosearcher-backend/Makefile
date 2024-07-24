up:
	docker-compose up -d --build

down:
	docker-compose down

process_video_frames:
	docker-compose exec -it videosearcher_backend sh -c "cd /app/video_processors && python video_frames_labeler.py"

logs:
	docker-compose logs -f

restart: down up
