var express = require('express');
var rpc_client = require('../rpc_client/rpc_client');
var router = express.Router();

/* GET news listing. */
router.get('/userId/:userId/pageNum/:pageNum', function(req, res, next) {
	console.log('Fetching news...');
	user_id = req.params['userid'];
	page_num = req.params['pageNum'];

	rpc_client.getNewsSummariesForUser(user_id, page_num, function(response) {
		res.json(response);
	});
});
// router.get('/', function(req, res, next) {
// 	news = [
// 				{
// 					'url': 'https://www.cnn.com/2018/07/08/asia/thai-cave-rescue-mission-intl/index.html',
// 					'title': "Rescuers up against 'water and time' to save remaining teammates trapped in Thai cave",
// 					'description': "The operation to rescue the remaining boys and their coach from a flooded cave in northern Thailand was expected to resume Monday morning, but heavy rain threatened to further complicate the mission.",
// 					'source': 'cnn',
// 					'urlToImage': 'https://cdn.cnn.com/cnnnext/dam/assets/180708083140-ny03-thailand-soccer-team-rescue-0708-ambulance-exlarge-169.jpg',
// 					'digest': "3RjuEomJo2601syZbU7OHA==\n",
// 					'reason': "Recommend"
// 				},
// 				{
// 					'title': 'Progressive Populism Can Save Us From Trump',
// 					'description': "The recent primary upset of Joe Crowley, the fourth-ranking Democrat in the House, by Alexandria Ocasio-Cortez, showcased the electoral strength of her platform, which included single-payer health insurance and tuition-free college and trade school. But soon afterward, Nancy Pelosi, the House minority leader, and Tammy Duckworth, a Democratic senator from Illinois, dismissed Ms. Ocasio-Cortez’s success as strictly a local phenomenon.",
// 					'url': "https://www.nytimes.com/2018/07/07/opinion/sunday/progressive-populism-wisconsin-trump.html?action=click&pgtype=Homepage&clickSource=story-heading&module=opinion-c-col-left-region&region=opinion-c-col-left-region&WT.nav=opinion-c-col-left-region",
// 					'urlToImage': "https://static01.nyt.com/images/2018/07/08/opinion/08kaufman/merlin_134552622_a2d14bfa-4365-4525-813d-9045c54c2b9a-superJumbo.jpg?quality=90&auto=webp",
// 					'source': 'nytimes',
// 					'digest': "3RjuEomJo2601syZbU7OHA=!\n",
// 					'time': "Today",
// 					'reason': "Hot"
// 				}
// 			]
// 	res.json(news);
// });

/* Log news click. */
router.post('/userId/:userId/newsId/:newsId', function(req, res, next) {
	console.log('Logging news click...');
	user_id = req.params['userId'];
	news_id = req.params['newsId'];

	rpc_client.logNewsClickForUser(user_id, news_id);
	res.status(200);
});

module.exports = router;