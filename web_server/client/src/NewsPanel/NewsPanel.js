import './NewsPanel.css';
import React from 'react';
import _ from 'lodash';
import Auth from '../Auth/Auth';

import NewsCard from '../NewsCard/NewsCard';

class NewsPanel extends React.Component {
	constructor() {
		super();
		this.state = {news:null, pageNum:1, totalPages:1, loadedAll:false};
		this.handleScroll = this.handleScroll.bind(this);
	}

	componentDidMount() {
		this.loadMoreNews();
		// all response within 1000 ms, treated as once
		this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
		window.addEventListener('scroll', this.handleScroll);
	}

	handleScroll() {
		// pick the first non-empty
		let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
		if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
			console.log('Loading more news');
			this.loadMoreNews();
		}
	}

	loadMoreNews(e) {
		if (this.state.loadedAll === true) {
			return;
		}
		// http://localhost:3000
		let url = '/news/userId/' + Auth.getEmail()
					+ '/pageNum/' + this.state.pageNum;

		let request = new Request(encodeURI(url), {
			method: 'GET',
			headers: {
				'Authorization': 'bearer ' + Auth.getToken(),
			},
			// cache: false
			cache: 'no-cache'
		});
		// let request = new Request('http://localhost:3000/news', {
		// 	method: 'GET',
		// 	headers: {
		// 		'Authorization': 'bearer ' + Auth.getToken(),
		// 	},
		// 	cache: false
		// });

		fetch(request)
			.then((res) => res.json())
			.then((news) => {
				if (!news || news.length === 0) {
					this.setState({loadedAll: true});
				}
				this.setState({
					news: this.state.news ? this.state.news.concat(news) : news,
					pageNum: this.state.pageNum + 1,
				});
			});
	}

	renderNews() {
		var news_list = this.state.news.map(function(news) {
			return (
				// <a className='list-group-item' href="#">
				<a className='list-group-item' key={news.digest} href="#">
					<NewsCard news={news} />
				</a>
				);
		});

		return (
			<div className="container-fluid">
			 <div className='list-group'>
			 	{news_list}
			 </div>
			</div>
			);
	}

	render() {
		if (this.state.news) {
			return (
					<div>
						{this.renderNews()}
					</div>
				);
		} else {
			return(
				<div>
					<div id='msg-app-loading'>
						Loading
					</div>
				</div>
			);
		}
	}
}

export default NewsPanel;